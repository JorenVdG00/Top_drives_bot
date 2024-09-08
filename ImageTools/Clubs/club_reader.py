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
