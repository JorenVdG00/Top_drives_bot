from PIL import Image
from ImageTools import pytesseract
from ImageTools.cropper.coords import club_coordinates, club_info_coords
from ImageTools.utils.image_utils import resize_image
from ImageTools.utils.file_utils import create_dir_if_not_exists
from ImageTools.utils.text_utils import remove_excessive_spaces, fix_missing_space
from config import BASE_DIR
def get_club_event_names(image_path):
    names = []
    x1, x2 = club_coordinates['club_events']['club_event_x']
    print(x1, x2)
    with Image.open(image_path) as image:
        resized_image = resize_image(image)
        for i in range(1, 5):
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


def crop_club_info(image_path, save_dir, name):
    # Set the full directory path
    full_dir = f'{save_dir}/{name}' if name else save_dir
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


save_dir = 'tst'
# test_img = 'clicked_event_2_req.png'
test_img = 'clicked_event.png'

event_name = get_club_name(test_img)
new_save_dir = (f'./tst')
crop_club_info(test_img, new_save_dir, event_name)
