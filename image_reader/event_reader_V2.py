from PIL import Image
import pytesseract
import re
import os
import itertools
import math
from image_enhancer import (full_image_enhancer)

condition_colors = {
    'SUN': (255, 232, 147, 255),
    'HIGH': (255, 114, 85, 255),
    'WET': (109, 208, 247, 255)
}

race_type_possibilities = [
    'G-FORCE TEST', 'MOUNTAIN SLALOM', '1/2 MILE DRAG', '1 MILE DRAG', '1/4 MILE DRAG',
    'KARTING CIRCUIT', '0-100MPH', 'FOREST ROAD', 'FOREST SLALOM', 'TWISTY ROAD', 'CANYON TOUR',
    'LOOKOUT', 'BUTTE', 'MOUNTAIN HILL CLIMB', 'MOUNTAIN HAIRPIN', 'MOUNTAIN INCLINE ROAD', 'FAST CIRCUIT'
]

road_type_possibilities = [
    'ASPHALT', 'SNOW', 'DIRT', 'MIXED', 'GRASS', 'SAND', 'ICE', 'GRAVEL'
]
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
def run_extraction_with_options(options, faulty_dirs):
    new_extracted_data = extract_event_types(faulty_dirs,
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
        possibilities = race_type_possibilities
    else:
        type = 'road_type'
        possibilities = road_type_possibilities

    for dir, races in extract_data.items():
        if races[type]:
            race_type = races[type]
            total += 1
            if race_type in possibilities:
                correct += 1
            else:
                if dir not in faults:
                    faults[dir] = {}
                faults[dir] = race_type
        else:
            if dir not in faults:
                faults[dir] = {}
            faults[dir] = None
    if faults == {}:
        return 1, None
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
    for dir, races in extract_data.items():
        for race_id, race_info in races.items():
            # Split and clean the 'race_type' and 'road_type' values
            race_info['race_type'] = race_info['race_type'].split('\n')[0].strip()
            race_info['road_type'] = race_info['road_type'].split('\n')[0].strip()
    return extract_data


def extract_event_types(dirs, denoise=False, deskew=False, grayscale=False, binarize=False, contrast=False,
                        sharpness=False):
    extract_data = {}
    for dir in dirs:
        if dir not in extract_data:
            extract_data[dir] = {}
        files = os.listdir(used_img_dir + dir)
        sorted_files = sorted(files)
        create_dir_if_not_exists(enhanced_dir, dir)
        for file in sorted_files:
            if file in ('conditions.png', 'event_number.png'):
                continue
            full_image_enhancer(used_img_dir + dir + '/' + file, enhanced_dir + dir + '/' + file, denoise=denoise,
                                deskew=deskew, grayscale=grayscale,
                                binarize=binarize, contrast=contrast, sharpness=sharpness)
            # Denoise, grayscale:  65% Correct
            # Denoise:  65% Correct
            img = Image.open(enhanced_dir + dir + '/' + file)
            fname = file.split('.')[0]
            extracted_text = pytesseract.image_to_string(img, config=custom_config)
            clean_text = extracted_text.split('\n')[0].strip()
            # print(extracted_text)
            extract_data[dir][fname] = clean_text
    return extract_data


def get_faulty_dirs(faults):
    faulty_dirs = []
    for dir, fault in faults.items():
        faulty_dirs.append(dir)
    return faulty_dirs


def solve_faults(preprocessing_options, faulty_dirs, is_race=True):
    # Initialize variables
    if is_race:
        type = 'race_type'
        possibilities = race_type_possibilities

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
        extracted_data = run_extraction_with_options(options, faulty_dirs)
        print(extracted_data)
        # Calculate percentage and faults
        percentage, faults = calculate_percentage_correct(extracted_data, is_race)
        print(faults)
        # Delete the correct ones out Faulty Dirs
        if faults is None:
            print('No faults detected')
        else:
            print('Faults:')
            for key, fault in faults.items():
                print(f'{key}: {fault}')
        if not faults:
            for key in faulty_dirs:
                correct_results[key] = extracted_data[key][type]
                faulty_dirs.remove(key)
        else:
            for key in faulty_dirs:
                print(key)
                if key not in faults:
                    print(f'{key}')
                    print(extracted_data[key])
                    correct_results[key] = extracted_data[key][type]
                    faulty_dirs.remove(key)
                else:
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


def complete_extraction(preprocessing_options, extract_data, is_race=True):
    percentage, faults = calculate_percentage_correct(extract_data, is_race)
    faulty_dir = get_faulty_dirs(faults)
    correct_results = solve_faults(preprocessing_options, faulty_dir, is_race)
    extract_data = change_data_to_correct_results(extract_data, correct_results, is_race)
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


def get_conditions(image_path, second_try=False):
    condition_dict = {}
    if second_try:
        condition_colors = {
            'SUN': (255, 232, 147, 255),
            'ROLLING': (255, 114, 85, 255),
            'WET': (109, 206, 245, 255)
        }
    for condition, color_code in condition_colors.items():
        if condition == 'ROLLING':
            if contains_color(image_path, color_code):
                if check_consecutive_pixels(image_path, color_code, required_consecutive=30):
                    condition_dict['HIGH'] = True
                else:
                    condition_dict['ROLLING'] = True
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


###DIRECTORIES###
test1_dir = 'AAAA/event_test_V2_cropped/RACING_TRIALS_-_STAGE_2/'
base_dir, name = split_path(test1_dir)
enhanced_dir = create_dir_if_not_exists(base_dir, (name + '_enhanced/'))
used_img_dir = test1_dir

dirs = get_directories(used_img_dir)
sorted_dirs = sorted(dirs)
extract_data = extract_event_types(sorted_dirs, sharpness=True)

race_type_complete_data = complete_extraction(preprocessing_options, extract_data)
all_type_complete_data = complete_extraction(preprocessing_options, race_type_complete_data, is_race=False)

perc, faults = calculate_percentage_correct(race_type_complete_data)
print('Race Type Percentage correct: ', perc)
for key, data in extract_data.items():
    print(f'{key}: {data}')
perc, faults = calculate_percentage_correct(race_type_complete_data, is_race=False)
print('Road Type Percentage correct: ', perc)

for dir in dirs:
    condition_dict = get_conditions(used_img_dir + dir + '/conditions.png')
    extract_data[dir]['conditions'] = []
    for key, value in condition_dict.items():
        if value:
            extract_data[dir]['conditions'].append(key)

for dir in extract_data.keys():
    if not extract_data[dir]['conditions']:
        condition_dict = get_conditions(used_img_dir + dir + '/conditions.png')

for key, value in extract_data.items():
    print(f'{key}: {value}')
