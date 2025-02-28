from config import logger, pytesseract
from app.utils.ImageTools.image_processing.image_enhancer import enhance_image
from ImageTools.extractors.extractor_base import extract_text
from utils.Brands.brand_utils import find_car_brands_in_str
import os
import re

top_options = {
    "option_1": {
        "invert": False,
        "brightness": True,
        "denoise": False,
        "deskew": False,
        "grayscale": False,
        "binarize": False,
        "contrast": True,
        "sharpness": True,
    },
    "option_2": {
        "invert": False,
        "brightness": True,
        "denoise": False,
        "deskew": False,
        "grayscale": False,
        "binarize": False,
        "contrast": True,
        "sharpness": False,
    },
    "option_3": {
        "invert": False,
        "brightness": True,
        "denoise": False,
        "deskew": False,
        "grayscale": True,
        "binarize": False,
        "contrast": True,
        "sharpness": False,
    },
    "option_4": {
        "invert": False,
        "brightness": True,
        "denoise": False,
        "deskew": True,
        "grayscale": False,
        "binarize": False,
        "contrast": True,
        "sharpness": True,
    },
    "option_5": {
        "invert": False,
        "brightness": True,
        "denoise": False,
        "deskew": False,
        "grayscale": True,
        "binarize": False,
        "contrast": True,
        "sharpness": True,
    },
    "option_6": {
        "invert": False,
        "brightness": True,
        "denoise": False,
        "deskew": False,
        "grayscale": True,
        "binarize": False,
        "contrast": True,
        "sharpness": False,
    },
    "option_7": {
        "invert": True,
        "brightness": True,
        "denoise": False,
        "deskew": False,
        "grayscale": False,
        "binarize": False,
        "contrast": False,
        "sharpness": True,
    },
    "option_8": {
        "invert": False,
        "brightness": False,
        "denoise": False,
        "deskew": False,
        "grayscale": False,
        "binarize": False,
        "contrast": False,
        "sharpness": True,
    },
    "option_9": {
        "invert": False,
        "brightness": False,
        "denoise": False,
        "deskew": False,
        "grayscale": False,
        "binarize": False,
        "contrast": False,
        "sharpness": False,
    },
    "option_10": {
        "invert": True,
        "brightness": False,
        "denoise": False,
        "deskew": False,
        "grayscale": False,
        "binarize": False,
        "contrast": False,
        "sharpness": False,
    },
}


def clean_string(string: str):
    """
    Cleans up a string by removing unwanted characters, such as line breaks and extra spaces.

    Args:
        string (str): The string to clean.

    Returns:
        str: The cleaned string.
    """
    return string.replace('\n', '').replace('\\', '').strip()

def remove_excessive_chars(string: str) -> str:
    return re.split(r'[~|%]', string, maxsplit=1)[0]


def is_year_pattern(string):
    try:
        year = int(string)
        if 1900 <= year <= 2100:
            return True
        else:
            return False
    except ValueError:
        return False
    
def find_year(string):
    filtered_string = str(extract_integers(string))
    if is_year_pattern(filtered_string):
        return filtered_string
    else:
        if len(filtered_string) > 4:
            if is_year_pattern(filtered_string[:4]):
                return filtered_string[:4]
            elif is_year_pattern(filtered_string[-4:]):
                return filtered_string[-4:]
            
        logger.error(f"Failed to extract year from string: {string}")
        return None
    
def extract_integers(s):
    # Find all digits in the string
    digit_strings = re.findall(r'\d', s)
    if digit_strings:
        # Join them together and convert to a single integer
        combined_integer = int(''.join(digit_strings))
        return combined_integer
    return None
  
def give_text_after_brand(string: str, brand: str):
    """
    Given a string and a brand, returns the text after the brand in the string.

    Args:
        string (str): The string to search in.
        brand (str): The brand to search for.

    Returns:
        str: The text after the brand in the string.
    """
    # string = clean_string(string)
    brand = brand.lower()
    split_string = string.lower().split()
    split_brand = brand.split()

    if len(split_brand) > 1:
        search_part = split_brand[-1]
    else:
        search_part = split_brand[0]

    # Find the index of the last part of the brand name in the string
    try:
        brand_index = split_string.index(search_part)
        return ' '.join(split_string[brand_index+1:])
    except ValueError:
        print(f"Failed to find {search_part} in {string}")
        # Attempt fuzzy matching if exact match fails
        for word in split_string:
            if search_part in word:
                brand_index = split_string.index(word)
                return ' '.join(split_string[brand_index+1:])

    return None  
# def give_text_after_brand(string: str, brand: str):
#     """
#     Given a string and a brand, returns the text after the brand in the string.

#     Args:
#         string (str): The string to search in.
#         brand (str): The brand to search for.

#     Returns:
#         str: The text after the brand in the string.
#     """
#     string = clean_string(string)
#     brand = brand.lower()
#     split_string = string.lower().split()
#     split_brand = brand.split()

#     if len(split_brand) > 1:
#         search_part = split_brand[-1]
#     else:
#         search_part = split_brand[0]
#     search_part = split_brand[-1] if len(split_brand) > 1 else split_brand[0]
#     for parts in split_string:
#         if '\n' in parts:
#             endstring = parts.split('\\')[0]
#             end_index = split_string.index(parts)
#             split_string[end_index] = endstring
#             break
#     if end_index is not None:
#         split_string = split_string[:end_index+1]    
    
#     if search_part in split_string:
#         return ' '.join(split_string[split_string.index(split_brand[0]):])
#     else:
#         print(f"Failed to find {search_part} in {string}")
#         for word in split_string:
#             if search_part in word:
#                 brand_index = split_string.index(word)
#                 break
#     return ' '.join(split_string[brand_index+1:])
    
    
    

def extract_brand_and_type(string: str):
    """
    Extracts the car brand and type from a given string.

    This function first cleans the input string and attempts to find a car brand
    within it. If a brand is found, it extracts the type of car following the brand
    and returns both the brand and the filtered car type.

    Args:
        string (str): The string to extract car brand and type from.

    Returns:
        tuple: A tuple containing the found car brand and the filtered car type.
               Returns None if no car brand is found.
    """
    # Clean the input string to remove unwanted characters
    string = clean_string(string)

    # Find the car brand in the string
    car_brand = find_car_brands_in_str(string)
    if not car_brand:
        return None, None  # Return None if no car brand is found

    # Convert the found brand to lowercase for consistent processing
    found_brand = car_brand.lower()

    # Extract the car type text that appears after the brand in the string
    car_type = give_text_after_brand(string, found_brand)

    # Filter out excessive characters from the car type
    filtered_car_type = remove_excessive_chars(car_type)

    # Return the found brand and filtered car type
    return found_brand, filtered_car_type



def run_text_extraction_with_10_combinations(name_img_path, year_img_path, save_img_path):
        
    """
    Runs text extraction on the given image paths using 10 different preprocessing
    option combinations. The function attempts to extract the car brand and type from
    the name image and the year from the year image. If any of the extractions fail,
    the function returns None for all extracted values. If all extractions succeed, the
    function returns a dictionary containing the extracted brand, type, and year.

    Args:
        name_img_path (str): The path of the image of the car name.
        year_img_path (str): The path of the image of the car year.
        save_img_path (str): The path where the enhanced images will be saved.

    Returns:
        dict: A dictionary containing the extracted car brand, type, and year.
              Returns None if any of the extractions fail.
    """

    car = {"brand": None, "type": None, "year": None}
    for i in range (1, 11):
        option = top_options[f"option_{i}"]
        if car["brand"] == None:
            enhance_image(name_img_path, save_img_path, **option)
            extracted_text = extract_text(save_img_path)
            brand, car_type = extract_brand_and_type(extracted_text)
            car["brand"] = brand
            car["type"] = car_type
        if car["year"] == None:        
            enhance_image(year_img_path, save_img_path, **option)
            extracted_text = extract_text(save_img_path)
            year = find_year(extracted_text)
            car["year"] = year

    if car["brand"] == None or car["type"] == None or car["year"] == None:
        car["brand"], car["type"], car["year"] = None, None, None
    ###Maybe delete
    # if car["brand"] == None or car["type"] == None or car["year"] == None:
    #     if car["brand"] == None:
    #         car["brand"], car["type"] = rerun_text_extraction_till_valid(name_img_path, save_img_path, is_name=True)
    #     if car["year"] == None:
    #         _, car["year"] = rerun_text_extraction_till_valid(year_img_path, save_img_path, is_name=False)
    return car