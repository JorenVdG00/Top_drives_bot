import re
from OLD.ImageTools import pytesseract
from OLD.Utils.image_utils import resize_image
from OLD.Utils.text_utils import remove_excessive_spaces
from OLD.ImageTools.cropper.coords import event_coordinates
from PIL import Image

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

def get_event_name(image_path):
    name_coords = event_coordinates['name']
    with Image.open(image_path) as image:
        resized_image = resize_image(image)
        cropped_image = resized_image.crop(name_coords)
        extract_name = pytesseract.image_to_string(cropped_image)
        event_name = extract_name[:-1]
        cleaned_event_name = remove_excessive_spaces(event_name)
        final_event_name = cleaned_event_name.replace(' ', '_')
        return final_event_name
