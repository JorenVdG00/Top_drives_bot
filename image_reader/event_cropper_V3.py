from unicodedata import category

from PIL import Image
import pytesseract
import re
import os

standard_size = (2210, 1248)
STANDARD_EVENT_IMG_SIZE = (330, 220)

event_coordinates = {
    "name": (650, 270, 1550, 350),
    "event_x": {
        "event_x_1": (170, 500),
        "event_x_2": (555, 885),
        "event_x_3": (940, 1270),
        "event_x_4": (1325, 1655),
        "event_x_5": (1710, 2040)
    },
    "event_y": {
        "event_y_1": (480, 700),
        "event_y_2": (840, 1060),
        "event_y_3": (590, 810),
        "event_y_4": (940, 1160)
    },
    "in_game_event_x": {
        "in_game_event_x_1": (210, 510),
        "in_game_event_x_2": (580, 880),
        "in_game_event_x_3": (950, 1250),
        "in_game_event_x_4": (1320, 1625),
        "in_game_event_x_5": (1700, 2000)
    },
    "in_game_event_y": (530, 745)
}

event_img_coords = {
    "race_type": (0, 5, 330, 50),
    "conditions": (5, 60, 320, 145),
    "event_number": (0, 150, 65, 215),
    "road_type": (75, 150, 330, 215)
}


# Function to classify the filenames
def classify_filename(filename):
    patterns = {
        '1': r'1-2\.png',
        '3': r'3-4\.png',
        'in_game': r'in_game\.png'
    }

    for category, pattern in patterns.items():
        if re.search(pattern, filename):
            print(f"Found {filename} in category {category}")
            return category
    return "No match"


# Function to resize an image to a standard size
def resize_image(image, standard_size=(2210, 1248)):
    return image.resize(standard_size, Image.Resampling.LANCZOS)


def crop_and_save_event_type_images(event_type_img_dir, save_dir):
    cats = []
    swap = False
    for filename in os.listdir(event_type_img_dir):
        category = classify_filename(filename)
        cats.append(category)

    print(len(cats))
    if ('1' in cats and '3' in cats) and (len(cats) == 2):
        print("Both 1 and 3 found or ingame found")
        if '1' in cats[0]:
            print('correct')
        else:
            print('swap')
            swap = True
            cats[0], cats[1] = cats[1], cats[0]
    elif 'in_game' in cats:
        print('in_game')
    else:
        print("give a dir with event_types and correct filenames")
        print("No 1 or 3 found")
        return
    name = 'name'
    dir = os.listdir(event_type_img_dir)
    if swap:
        dir[0], dir[1] = dir[1], dir[0]
    for filename in dir:
        img_path = os.path.join(event_type_img_dir, filename)
        category = classify_filename(img_path)
        print(category)
        image = Image.open(img_path)
        image = resize_image(image, standard_size)

        if category == 'No match':
            print(f"No match found for {img_path}")
            break
        if category == 'in_game':
            crops_ingame_event_types(image, save_dir)
        elif category == '1':
            event_number = int(category[-1])
            name = extract_name_event(image, save_dir)
            create_dir_if_not_exists(save_dir, name)
            crop_event_types(image, save_dir, name, event_number)
            event_number += 1
            crop_event_types(image, save_dir, name, event_number)

        elif category == '3':
            event_number = int(category[-1])
            crop_event_types(image, save_dir, name, event_number)
            event_number += 1
            crop_event_types(image, save_dir, name, event_number)


def create_dir_if_not_exists(parent_dir, sub_dir):
    # Create the full path for the subdirectory
    full_path = os.path.join(parent_dir, sub_dir)

    # Check if the directory already exists
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        print(f"Directory '{full_path}' created.")
    else:
        print(f"Directory '{full_path}' already exists.")


def crops_ingame_event_types(image, save_dir, name=None):
    y1, y2 = event_coordinates['in_game_event_y']
    print(y1, y2)
    i = 1
    for xcoords in event_coordinates['in_game_event_x'].values():
        x1, x2 = xcoords
        cropped_image = image.crop((x1, y1, x2, y2))
        if name:
            cropped_image.save(f"{save_dir}/{name}/{i}.png")
        else:
            cropped_image.save(f"{save_dir}/In_game_cropped-{i}.png")
        i += 1


def extract_name_event(image, save_dir):
    name_coords = event_coordinates['name']
    cropped_image = image.crop(name_coords)
    extract_name = pytesseract.image_to_string(cropped_image)
    event_name = extract_name[:-1]
    cleaned_event_name = clean_string(event_name)
    final_event_name = cleaned_event_name.replace(' ', '_')
    create_dir_if_not_exists(save_dir, final_event_name)
    # NOT USEFULL
    # cropped_image.save(f"{save_dir}/{event_name}/name.png")
    return final_event_name


def crop_event_types(image, save_dir, name, event_number):
    i = 1
    y1, y2 = event_coordinates['event_y'][f'event_y_{event_number}']
    for xcoords in event_coordinates['event_x'].values():
        x1, x2 = xcoords
        cropped_image = image.crop((x1, y1, x2, y2))
        event_img_dir = f"{save_dir}/{name}"
        create_dir_if_not_exists(event_img_dir, f'{event_number}-{i}')
        img_dir = f"{event_img_dir}/{event_number}-{i}"
        crop_event_imgs(cropped_image, img_dir)
        i += 1


def crop_event_imgs(img, save_dir):
    for key, coords in event_img_coords.items():
        cropped_image = img.crop(coords)
        cropped_image.save(f"{save_dir}/{key}.png")


def clean_string(input_string):
    # This regex replaces multiple spaces between words with a single space
    # and removes trailing spaces at the end of the string
    cleaned_string = re.sub(r'\s+', ' ', input_string).strip()
    return cleaned_string


# crop_and_save_event_type_images('./event_test/In_game', './event_test/In_game_cropped')
crop_and_save_event_type_images('./event_test_V2/new', 'AAAA/event_test_V2_cropped')
