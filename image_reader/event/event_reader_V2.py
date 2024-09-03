from PIL import Image
import pytesseract
import re
import os
import itertools
import math
from image_reader.image_enhancer import full_image_enhancer
import csv
from config import TRACK_NAMES_PATH
from dotenv import load_dotenv

load_dotenv()

track_names = set()
track_names_path = TRACK_NAMES_PATH
pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_PATH')

with open(track_names_path, mode='r', newline='') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        track_names.add(row[0].strip())


# Check if any track name is in a given string and return the found track name
def contains_track_name(s):
    for track_name in track_names:
        if track_name in s:
            return track_name
    return None


# race_type_possibilities = [
#     'G-FORCE TEST', 'MOUNTAIN SLALOM', '1/2 MILE DRAG', '1 MILE DRAG', '1/4 MILE DRAG',
#     'KARTING CIRCUIT', '0-100MPH', '0-150MPH', 'CAR PARK', 'CITY STREETS SMALL', 'CITY STREETS MEDIUM', 'FOREST ROAD',
#     'FOREST SLALOM', 'TWISTY ROAD', 'CANYON TOUR', 'FAST CIRCUIT', 'TWISTY CIRCUIT',
#     'LOOKOUT', 'BUTTE', 'MOUNTAIN HILL CLIMB', 'MOUNTAIN HAIRPIN', 'MOUNTAIN INCLINE ROAD', 'FAST CIRCUIT'
# ]

road_type_possibilities = [
    'ASPHALT', 'SNOW', 'DIRT', 'MIXED', 'GRASS', 'SAND', 'ICE', 'GRAVEL'
]

condition_colors = {
    'SUN': (255, 232, 147, 255),
    'HIGH': (255, 114, 85, 255),
    'WET': (109, 208, 247, 255)
}

custom_config = r'--oem 3 --psm 6'

preprocessing_options = {
    'denoise': [True, False],
    'deskew': [True, False],
    'grayscale': [True, False],
    'binarize': [True, False],
    'contrast': [True, False],
    'sharpness': [True, False]
}


# Function to run extractions with given preprocessing options
def run_extraction_with_options(options, faulty_dirs, used_img_dir, enhanced_dir):
    new_extracted_data = extract_event_types(faulty_dirs, used_img_dir, enhanced_dir,
                                             denoise=options['denoise'],
                                             deskew=options['deskew'],
                                             grayscale=options['grayscale'],
                                             binarize=options['binarize'],
                                             contrast=options['contrast'],
                                             sharpness=options['sharpness'])
    return new_extracted_data


def calculate_percentage_correct(extract_data, is_race=True):
    total = 0
    correct = 0
    faults = {}
    if is_race:
        type = 'race_type'
        possibilities = track_names
    else:
        type = 'road_type'
        possibilities = road_type_possibilities
    for dir, races in extract_data.items():
        if races[type]:
            race_type = races[type]
            total += 1
            if race_type in possibilities:
                is_correct = True
                for possibility in possibilities:
                    if possibility not in race_type and race_type in possibility:
                        if dir not in faults:
                            faults[dir] = race_type
                            is_correct = False
                            continue
                if is_correct:
                    correct += 1

            else:
                if dir not in faults:
                    faults[dir] = {}
                faults[dir] = race_type
        else:
            if dir not in faults:
                faults[dir] = {}
            print("No fault detected")
            faults[dir] = None
    if faults == {}:
        print("No faults detected")
        return 1, None
    for dir, fault in faults.items():
        print("Fault detected")
        if fault:
            print(f'{dir}: {fault}')
    return correct / total, faults


def split_path(path):
    # Remove trailing slashes if any
    path = path.rstrip('/')

    # Split the path into head (rest of the path) and tail (last directory name)
    head, tail = os.path.split(path)

    return head, tail


def create_dir_if_not_exists(parent_dir, sub_dir):
    # Create the full path for the subdirectory
    full_path = os.path.join(parent_dir, sub_dir)

    # Check if the directory already exists
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        print(f"Directory '{full_path}' created.")
    else:
        print(f"Directory '{full_path}' already exists.")

    return full_path


def get_directories(directory):
    # List all items in the directory
    all_items = os.listdir(directory)

    # Filter out the directories
    dirs = [item for item in all_items if os.path.isdir(os.path.join(directory, item))]

    return dirs


def clean_data(extract_data):
    for dir, race_info in extract_data.items():
        # Split and clean the 'race_type' and 'road_type' values
        race_info['race_type'] = race_info['race_type'].split('\n')[0].strip()
        circuit = race_info['race_type'].split('\n')[0].strip()

        if 'MPH' in circuit:
            circuit = replace_o_with_zero(circuit)

        for road in road_type_possibilities:
            if road in race_info['road_type']:
                race_info['road_type'] = road
        for track in track_names:
            if track in circuit:
                race_info['race_type'] = track
    return extract_data


def replace_o_with_zero(race_str):
    """Replace 0 with O in the string to handle confusion."""
    return race_str.replace('O', '0')


def fix_missing_space(race_str, possibilities):
    """Attempts to fix missing spaces in a race string based on known possibilities."""

    # Remove spaces to simulate the input with missing spaces
    condensed_race_str = race_str.replace(" ", "")

    for possibility in possibilities:
        if not "MPH" in possibility:
            print(f"Possible missing space in {possibility}")
            continue
        condensed_possibility = possibility.replace(" ", "")
        print(condensed_possibility)
        possibility_0 = replace_o_with_zero(condensed_possibility)
        race_str_0 = replace_o_with_zero(condensed_race_str)
        print("race_str_O", race_str_0)
        if "0-100" in possibility_0:
            print("possibility_O", possibility_0)
        # Check if the condensed race string matches the condensed possibility
        if possibility_0 == race_str_0:
            return possibility  # Return the correctly formatted possibility

    # If no match is found, return the original string
    return None


def extract_event_types(dirs, used_img_dir, enhanced_dir, denoise=False, deskew=False, grayscale=False, binarize=False,
                        contrast=False,
                        sharpness=False, double_lines=False):
    extract_data = {}
    for dir in dirs:
        if dir not in extract_data:
            extract_data[dir] = {}
        files = os.listdir(used_img_dir + dir)
        sorted_files = sorted(files)
        create_dir_if_not_exists(enhanced_dir, dir)
        for file in sorted_files:
            if file in ('conditions.png', 'event_number.png', 'full_race.png'):
                continue
            full_image_enhancer(used_img_dir + dir + '/' + file, enhanced_dir + dir + '/' + file, denoise=denoise,
                                deskew=deskew, grayscale=grayscale,
                                binarize=binarize, contrast=contrast, sharpness=sharpness)
            # Denoise, grayscale:  65% Correct
            # Denoise:  65% Correct
            img = Image.open(enhanced_dir + dir + '/' + file)
            fname = file.split('.')[0]
            extracted_text = pytesseract.image_to_string(img, config=custom_config)
            # clean_text = extracted_text.split('\n')[0].strip()
            words = extracted_text.replace('\n', ' ').split(' ')
            # Remove empty strings
            filtered_words = [word for word in words if word]

            # Join the words with a space
            result = ' '.join(filtered_words)
            print(result)
            extract_data[dir][fname] = result
            # if 'LUMBER MILL FOREST' in extracted_text:
            #     print(extracted_text)
            #     print(extracted_text)
            #     # print("head: " + head)
            #     # print("tail: " + tail)
            #     # print("merge_text: " + merge_text)
            #     words = extracted_text.replace('\n', ' ').split(' ')
            #     # Remove empty strings
            #     filtered_words = [word for word in words if word]
            #
            #     # Join the words with a space
            #     result = ' '.join(filtered_words)
            #     print(result)
            #     extract_data[dir][fname] = result
            # else:
            #     extract_data[dir][fname] = clean_text

    return extract_data


def get_faulty_dirs(faults):
    faulty_dirs = []
    for dir, fault in faults.items():
        faulty_dirs.append(dir)
    return faulty_dirs


def solve_faults(preprocessing_options, faulty_dirs, used_img_dir, enhanced_dir, is_race=True):
    # Initialize variables
    if is_race:
        type = 'race_type'
        possibilities = track_names

    else:
        type = 'road_type'
        possibilities = road_type_possibilities

    ## Generate all possible combinations of preprocessing options
    combinations = list(itertools.product(*preprocessing_options.values()))

    # Store results
    results = {}

    correct_results = {}
    # Iterate through each combination
    for combination in combinations:
        options = dict(zip(preprocessing_options.keys(), combination))
        print(f"Testing with options: {options}")

        # Run extraction with the current options
        extracted_data = run_extraction_with_options(options, faulty_dirs, used_img_dir, enhanced_dir)
        cleaned_data = clean_data(extracted_data)
        # Calculate percentage and faults
        percentage, faults = calculate_percentage_correct(cleaned_data, is_race)
        print(faults)
        # Delete the correct ones out Faulty Dirs
        if faults is None:
            print('No faults detected')
            break
        else:
            print('Faults:')
            for key, fault in faults.items():
                print(f'{key}: {fault}')
        if not faults:
            for key in faulty_dirs:
                correct_results[key] = cleaned_data[key][type]
                faulty_dirs.remove(key)
        else:
            for key in faulty_dirs:
                print(key)
                if key not in faults:
                    print(f'{key}')
                    print(extracted_data[key])
                    correct_results[key] = cleaned_data[key][type]
                    faulty_dirs.remove(key)
                else:
                    if is_race:
                        if type == 'race_type':
                            # print('B\n'*10)
                            # print(extracted_data[key][type])
                            # correct_str = fix_missing_space(extracted_data[key][type], track_names)
                            # print(correct_str)
                            # if correct_str:
                            #     print('correct:', correct_str)
                            #     correct_results[key] = correct_str
                            #     faulty_dirs.remove(key)
                            #     break
                            track_name = contains_track_name(cleaned_data[key][type])
                            if track_name:
                                correct_results[key] = track_name
                                faulty_dirs.remove(key)
                                break

                    for possible in possibilities:
                        if possible in faults[key]:
                            correct_results[key] = possible
                            faulty_dirs.remove(key)
                            break

        # Store the results
        results[str(options)] = {'percentage': percentage, 'faults': faults}
    return correct_results


def change_data_to_correct_results(extract_data, correct_results, is_race=True):
    if is_race:
        type = 'race_type'
    else:
        type = 'road_type'
    for dir in correct_results:
        extract_data[dir][type] = correct_results[dir]
    return extract_data


def complete_extraction(preprocessing_options, extract_data, used_img_dir, enhanced_img_dir, is_race=True):
    percentage, faults = calculate_percentage_correct(extract_data, is_race)
    print(faults)
    if faults:
        faulty_dir = get_faulty_dirs(faults)
        correct_results = solve_faults(preprocessing_options, faulty_dir, used_img_dir, enhanced_img_dir, is_race)
        extract_data = change_data_to_correct_results(extract_data, correct_results, is_race)
    else:
        print("No faults found")
    return extract_data


def contains_color(image_path, target_rgb, tolerance=5):
    image = Image.open(image_path)
    pixels = image.load()

    # Loop through the pixels and check for the target color
    for x in range(image.width):
        for y in range(image.height):
            if color_distance(pixels[x, y], target_rgb) <= tolerance:
                return True
    return False


def get_conditions(image_path):
    condition_dict = {}
    for condition, color_code in condition_colors.items():
        if condition == 'HIGH':
            if contains_color(image_path, color_code):
                if check_consecutive_pixels(image_path, color_code, required_consecutive=30):
                    condition_dict['HIGH'] = True
                    condition_dict['ROLLING'] = False
                else:
                    condition_dict['ROLLING'] = True
                    condition_dict['HIGH'] = False
        else:
            condition_dict[condition] = contains_color(image_path, color_code)

    return condition_dict


def color_distance(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1[:3], c2[:3])))  # Ignore the alpha channel


# Function to check if there are 30 consecutive pixels matching the filter color along the y-axis
def check_consecutive_pixels(image_path, filter_color, tolerance=10, required_consecutive=30):
    image = Image.open(image_path).convert('RGBA')
    width, height = image.size

    for y in range(height):
        consecutive_count = 0
        for x in range(width):
            pixel_color = image.getpixel((x, y))
            if color_distance(pixel_color, filter_color) <= tolerance:
                consecutive_count += 1
                if consecutive_count >= required_consecutive:
                    return True  # Found 30 consecutive matching pixels
            else:
                consecutive_count = 0  # Reset the count if the color doesn't match

    return False  # No matching sequence found


def get_full_event_type_list(events_dir):
    extract_data = {}
    base_dir, name = split_path(events_dir)
    enhanced_dir = create_dir_if_not_exists(base_dir, 'enhanced/')
    used_img_dir = events_dir

    dirs = get_directories(used_img_dir)
    sorted_dirs = sorted(dirs)
    print(used_img_dir * 20)
    extract_data = extract_event_types(sorted_dirs, used_img_dir, enhanced_dir, sharpness=True)
    cleaned_data = clean_data(extract_data)

    race_type_complete_data = complete_extraction(preprocessing_options, cleaned_data, used_img_dir, enhanced_dir)
    all_type_complete_data = complete_extraction(preprocessing_options, race_type_complete_data, used_img_dir,
                                                 enhanced_dir, is_race=False)

    for dir in dirs:
        condition_dict = get_conditions(used_img_dir + dir + '/conditions.png')
        extract_data[dir]['conditions'] = condition_dict

    return extract_data


def get_ingame_race_tracks(dir):
    extract_data = {}
    used_img_dir = dir
    base_dir, name = split_path(dir)
    enhanced_dir = create_dir_if_not_exists(base_dir, 'enhanced/')
    dirs = get_directories(used_img_dir)
    sorted_dirs = sorted(dirs)
    extract_data = extract_event_types(sorted_dirs, used_img_dir, enhanced_dir, sharpness=True)
    cleaned_data = clean_data(extract_data)

    race_type_complete_data = complete_extraction(preprocessing_options, cleaned_data, used_img_dir, enhanced_dir)
    return race_type_complete_data

# get_full_event_type_list('../tests/test_granD_c_cropped/GRAND_CANYON/')
