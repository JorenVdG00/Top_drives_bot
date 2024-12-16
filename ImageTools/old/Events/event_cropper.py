import os
from PIL import Image
from ImageTools.cropper.classify import get_event_name, classify_filename
from ImageTools.cropper.coords import event_coordinates, event_img_coords, display_img_coords, last_display_img_coords
from ImageTools.utils.image_utils import resize_image
from ImageTools.utils.file_utils import create_dir_if_not_exists
from ImageTools.image_processing.cropper import crop_image


def crop_and_save_event_type_images(event_type_img_dir, save_dir):
    cats = []  # Categories
    swap = False
    event_number = 0
    for filename in os.listdir(event_type_img_dir):
        category = classify_filename(filename)
        cats.append(category)

    if ('1' in cats and '3' in cats) and (len(cats) == 2):
        print("Both 1 and 3 found found")
        if '1' in cats[0]:
            print('correct')
        else:
            print('swap')
            swap = True
            cats[0], cats[1] = cats[1], cats[0]
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
        if category == '1':
            name = get_event_name(img_path)
            create_dir_if_not_exists(save_dir, name)
            event_number = int(category[-1])
        crop_event_types(img_path, save_dir, name, event_number)
        event_number += 1
        crop_event_types(img_path, save_dir, name, event_number)
        event_number += 1


def crop_event_types(image_path, save_dir, name, event_number):
    race_number = 1
    y1, y2 = event_coordinates['event_y'][f'event_y_{event_number}']
    for xcoords in event_coordinates['event_x'].values():
        x1, x2 = xcoords
        coords = (x1, y1, x2, y2)
        save_path = f'{save_dir}/{name}/{event_number}-{race_number}/'
        race_path = crop_image(image_path, save_path, 'full_race', coords)
        crop_race_in_parts(race_path, save_path)
        race_number += 1


def crop_in_game_event_types(img_path, save_dir, name=None):
    if name:
        img_dir = f"{save_dir}/{name}/"
        create_dir_if_not_exists(save_dir, name)
    else:
        img_dir = f"{save_dir}/"
        create_dir_if_not_exists(save_dir)
    race_number = 1
    y1, y2 = event_coordinates['in_game_event_y']
    for xcoords in event_coordinates['in_game_event_x'].values():
        x1, x2 = xcoords
        coords = (x1, y1, x2, y2)
        save_dir = f'{img_dir}/{race_number}'
        race_path = crop_image(img_path, save_dir, 'full_race', coords)
        crop_race_in_parts(race_path, save_dir)
        race_number += 1


def crop_race_in_parts(img_path, save_dir):
    create_dir_if_not_exists(save_dir)
    with Image.open(img_path) as image:
        for key, coords in event_img_coords.items():
            cropped_image = image.crop(coords)
            cropped_image.save(f"{save_dir}/{key}.png")


def crop_event_display_img(img_path, save_dir, name, last=False):
    if last:
        display_path = crop_image(img_path, save_dir, name, last_display_img_coords)
    else:
        display_path = crop_image(img_path, save_dir, name, display_img_coords)
    return display_path
