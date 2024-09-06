from PIL import Image
from ImageTools import pytesseract
from ImageTools.utils.file_utils import get_directories, get_files, get_head
from ImageTools.utils.text_utils import remove_newlines
from ImageTools.utils.image_utils import contains_color
from ImageTools.Clubs.club_cropper import get_club_name
from ImageTools.image_processing.extractor import extract_text_from_image
from database.db_getters import get_club_reqs
import os
import re
from config import BASE_DIR

# Example patterns
# patterns = {'event_type_pattern': r'^[A-Z\s]+$',
#             'name_pattern': r' ^ [A - Z\s]+\d +$',
#             'player_amount_pattern': r'^([1-9][0-9]?|1[0-4][0-9]|150)$',
#             'reqs_pattern': r'^[A-Z]{2,4}\sx[2-5]$',
#             'rq_pattern': r'^[A-Z]{2}\s([1-4]?[0-9]{1,2}|500)$',
#             'score_pattern': r'^([1-9][0-9]{2,3}|10000)$',
#             'time_left_pattern': r'^\d+h\s\d+m\s\d+s$',
#             'weight_pattern': r'^\d{2,4}$'}

path = f'{BASE_DIR}/ImageTools/Clubs/tst/clubInfo/LEGACY_65'


# def clean_input(input_string, pattern):
#     match = re.match(pattern, input_string)
#     if match:
#         return match.group(0)  # Return the matched part
#     else:
#         # If there's no match, try to extract the correct part
#         corrected = re.findall(pattern, input_string)
#         return corrected[0] if corrected else None
#

def extract_club_info(club_dir):
    extracted_dict = {}
    files = get_files(club_dir)
    if files:
        for file_name in files:
            if file_name.endswith('.png'):
                head = get_head(file_name)
                extracted_text = extract_text_from_image(f'{club_dir}/{file_name}')
                no_newlines = remove_newlines(extracted_text)
                extracted_dict[head] = no_newlines
    return extracted_dict


extracted_dict = extract_club_info(path)
for key, value in extracted_dict.items():
    print(f'{key}: {value}')

def req_met(club_dir):
    has_req_color = (251, 251, 251, 255)
    met_req_color = (0, 237, 1, 255)
    files = get_files(club_dir)
    for file_name in files:
        if 'reqs' in file_name:
            file_path = f'{club_dir}/{file_name}'
            if contains_color(file_path, has_req_color):
                if contains_color(file_path, met_req_color, tolerance=10):
                    continue
                else:
                    return False
    return True



reqs = get_club_reqs()
print(reqs)