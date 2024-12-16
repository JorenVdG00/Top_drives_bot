import os

from PIL import Image
from ImageTools import pytesseract
from ImageTools.cropper.coords import club_coordinates, club_info_coords, in_event_club_info_coords
from ImageTools.Clubs.clean_clubs import fix_reqs, fix_rq_value, cut_until_integer
from ImageTools.utils.image_utils import resize_image
from ImageTools.utils.file_utils import create_dir_if_not_exists
from ImageTools.utils.text_utils import remove_excessive_spaces, fix_missing_space
from database.methods.db_events import get_req_id
from config import BASE_DIR
def get_club_event_names(image_path):
    names = []
    x1, x2 = club_coordinates['club_events']['club_event_x']
    print(x1, x2)
    with Image.open(image_path) as image:
        resized_image = resize_image(image)
        for i in range(1, 4):
            y1, y2 = club_coordinates['club_events']['club_event_y'][f'club_event_y{i}']
            print(y1, y2)
            crop_coords = (int(x1), int(y1), int(x2), int(y2))
            print(f'cropcoords: {crop_coords}')
            cropped_image = resized_image.crop(crop_coords)
            extract_name = pytesseract.image_to_string(cropped_image)
            split_name = extract_name.split('\n')[0]
            names.append(split_name)
    return names

def get_club_name(image_path):
    with Image.open(image_path) as image:
        resized_image = resize_image(image)
        cropped_image = resized_image.crop(club_info_coords['name'])
        extract_name = pytesseract.image_to_string(cropped_image)
        print(extract_name)
        event_name = extract_name[:-1]
        cleaned_event_name = remove_excessive_spaces(event_name)
        final_event_name = cleaned_event_name.replace(' ', '_')
    return final_event_name


def crop_club_info(image_path, save_dir):
    club_event_name = get_club_name(image_path)
    # Set the full directory path
    full_dir = f'{save_dir}/{club_event_name}'
    create_dir_if_not_exists(full_dir)

    # Open the image and resize it
    with Image.open(image_path) as image:
        resized_image = resize_image(image)

        # Loop through the coordinates for cropping
        for key, coords in club_info_coords.items():
            if isinstance(coords, dict):
                # Handle nested dictionaries for 'player_amount' and 'score'
                y1, y2 = coords['y']
                for sub_key in ['left_x', 'right_x']:
                    x1, x2 = coords[sub_key]
                    crop_box = (x1, int(y1), int(x2), int(y2))
                    cropped_image = resized_image.crop(crop_box)
                    cropped_image.save(f'{full_dir}/{key}-{sub_key}.png')
                    print(f'image saved: {full_dir}/{key}-{sub_key}.png')

            else:
                # Handle simple coordinates for other keys
                x1, y1, x2, y2 = coords
                crop_box = (x1, y1, x2, y2)
                cropped_image = resized_image.crop(crop_box)
                cropped_image.save(f'{full_dir}/{key}.png')
                print(f'image saved: {full_dir}/{key}.png')
    return full_dir



def crop_in_event_club_info(image_path):
    club_info_dict = {}
    with Image.open(image_path) as image:
        resized_image = resize_image(image)
        name_coords = in_event_club_info_coords['names']
        rq_coords = in_event_club_info_coords['rq']
        req1_coords = in_event_club_info_coords['reqs1']
        req2_coords = in_event_club_info_coords['reqs2']

        name_cropped_image = resized_image.crop(name_coords)
        extract_name = pytesseract.image_to_string(name_cropped_image)

        split_name = extract_name.split('-')
        event_name, event_type = split_name[0], split_name[1]

        cleaned_event_name = remove_excessive_spaces(event_name)
        final_event_name = cleaned_event_name.replace(' ', '_')

        cleaned_event_type = remove_excessive_spaces(event_type)
        final_event_type = cleaned_event_type.replace(' ', '_')
        club_info_dict['event_name'] = final_event_name
        club_info_dict['event_type'] = final_event_type

        rq_cropped_image = resized_image.crop(rq_coords)
        rq_extract = pytesseract.image_to_string(rq_cropped_image)
        fixed_rq = fix_rq_value(rq_extract)
        club_info_dict['rq'] = fixed_rq

        req1_cropped_image = resized_image.crop(req1_coords)
        req2_cropped_image = resized_image.crop(req2_coords)
        req_list = []

        req_list.append(pytesseract.image_to_string(req1_cropped_image))
        req_list.append(pytesseract.image_to_string(req2_cropped_image))

        for i in range(2):
            club_info_dict[f'req{i+1}_id'] = None

        index = 1
        for req in req_list:
            cutted_str = cut_until_integer(req)
            req_split = cutted_str.rsplit(' ', 1)
            print(req_split)
            if len(req_split) >= 2:
                req_name, req_number = req_split[0], req_split[1][-1]
                print(f'{req_name} {req_number}')
                req_id = get_req_id(req_name)
                club_info_dict[f'req{index}_id'] = req_id
                index += 1

    return club_info_dict


if __name__ == '__main__':
    img_path = './tst/in_club_event_cropper.png'
    img_path2 = './tst/in_club_event_cropper2.png'
    data_dict1 = crop_in_event_club_info(img_path)
    data_dict2 = crop_in_event_club_info(img_path2)
    for key, value in data_dict1.items():
        print(key, value)
    print('\n')
    for key, value in data_dict2.items():
        print(key, value)