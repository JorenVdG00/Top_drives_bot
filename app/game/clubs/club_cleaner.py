from enum import Enum
from config import logger
from app.utils.ImageTools.image_utils import contains_color
from utils.text_utils import  extract_integers, cut_until_integer, remove_excessive_spaces, replace_spaces, remove_newlines

class TeamColor(Enum):
    FULL_THROTTLE = (203, 119, 86, 255)
    LEGACY = (255, 247, 177, 255)
    MIDNIGHT = (74, 136, 163, 255)

SIDES = ['left', 'right']

    
def weight_to_team(image):
    """
    Determines the team based on the predominant color found in the image.

    Iterates through predefined team colors and checks if the image contains
    any of these colors. Returns the name of the team if a match is found.
    Logs a debug message and returns None if no team color is detected.

    Args:
        image (Image): The image to be analyzed for team color.

    Returns:
        str or None: The name of the team if a matching color is found,
        otherwise None.
    """
    for team in TeamColor:
        if contains_color(image, team.value):
            return team.name
    logger.debug("No team color found")
    return None

def correct_weight_value(weight_string: str)-> int:
    """
    Corrects the weight value extracted from a string by removing
    any extra leading digits. If no integers are found in the string,
    returns a default value of 5.

    Args:
        weight_string (str): The input string from which the weight
        value is extracted.

    Returns:
        int: The corrected weight value as an integer.
    """
    value = extract_integers(weight_string)
    if value is None:
        return 5
    if len(str(value)) > 1:
        fixed_value = str(value)[1:]
    else:
        fixed_value = str(value)
    return int(fixed_value)


def fix_rq_value(rq_string: str)-> int:
    """
    Corrects the RQ value extracted from a string by removing
    any extra non-numeric characters. If no integers are found in the string,
    returns None.

    Args:
        string (str): The input string from which the RQ value is extracted.

    Returns:
        int or None: The corrected RQ value as an integer if a numeric value is found,
        otherwise None.
    """
    correct_rq = extract_integers(rq_string)
    return correct_rq


def fix_score_value(extracted_data: dict)-> dict:
    """
    Corrects the score values in the extracted data by converting them to integers. If the score value is None or cannot be converted to an integer, sets it to 5000.

    Args:
        extracted_data (dict): The extracted data containing the score values to be corrected.

    Returns:
        dict: The corrected extracted data with the score values as integers.
    """
    
    for side in SIDES:
        score = extracted_data[f'score_{side}']
        extracted_data[f'score_{side}'] = extract_integers(score)
        if extracted_data[f'score_{side}'] is None:
            extracted_data[f'score_{side}'] = 5000     
    return extracted_data


def fix_reqs(extracted_data: dict)-> dict:
    """
    Corrects the requirement values in the extracted data by converting them to dictionaries with keys 'name' and 'number'. If the requirement value is None or cannot be converted to a dictionary, sets it to {'name': 'NONE', 'number': '0'}.

    Args:
        extracted_data (dict): The extracted data containing the requirement values to be corrected.

    Returns:
        dict: The corrected extracted data with the requirement values as dictionaries.
    """
    for i in range(1, 3):
        req_str = extracted_data[f'reqs{i}']
        if len(req_str) > 2:
            cutted_str = cut_until_integer(req_str)
            if extract_integers(cutted_str) is None:
                extracted_data[f'reqs{i}'] = {'name': 'NONE', 'number': '0'} 
                continue
            req_split = cutted_str.rsplit(' ', 1)
            logger.debug('req_split: ' + str(req_split))
            req_name, req_number = req_split[0], req_split[1][-1]
            req_number = extract_integers(req_number)
        else:
            req_name, req_number = '', 0
        extracted_data[f'reqs{i}'] = {'name': req_name, 'number': req_number}
    return extracted_data


def has_req_met(image)-> str:
    """Determines if a requirement has been met by checking the color of the requirement check box.

    Args:
        image PIL.Image: The image of the requirement check box.

    Returns:
        str: 'MET' if the requirement has been met, 'NOT_MET' if it has not, or 'NONE' if the image does not contain the requirement check box.
    """
    reqs_met_color = (0, 244, 0, 255)
    reqs_not_met_color = (112, 118, 131, 255)
    # reqs_not_met_color = (117, 123, 135, 255)
    if contains_color(image, reqs_met_color, tolerance=10):
        return 'MET'
    elif contains_color(image, reqs_not_met_color, tolerance=10):
        return 'NOT_MET'
    else:
        return 'NONE'
    


def fix_players(extracted_data):
    for side in SIDES:
        xamount = str(extracted_data[f'players_{side}']).replace(" ", "")
        if '/150' in xamount:
            extracted_data[f'players_{side}'] = xamount.split('/')[0]
            continue
        amount = cut_until_integer(xamount)
        if len(amount) == 0:
            extracted_data[f'players_{side}'] = 0
    return extracted_data




def fix_extracted_data(extracted_data):
    for key, value in extracted_data.items():
        logger.debug(f'{key}:  {value}')
    
    # fix player_amounts
    extracted_data = fix_players(extracted_data)

    # fix requirements
    extracted_data = fix_reqs(extracted_data)

    print(extracted_data.get('score_left'))
    # fix scores
    extracted_data = fix_score_value(extracted_data)

    # fix rq
    extracted_data['rq'] = fix_rq_value(extracted_data['rq'])
    # fix weight value because it add a number too much
    extracted_data['weight'] = correct_weight_value(extracted_data['weight'])

    return extracted_data


def fix_short_data(extracted_data: dict[str, str])-> dict[str, str]:
    extracted_data = fix_reqs(extracted_data)
    extracted_data['rq'] = fix_rq_value(extracted_data['rq'])
    return extracted_data


def clean_extracted_club_name(name: str)-> str:
    cleaned_name = remove_newlines(name)
    removed_spaces = remove_excessive_spaces(cleaned_name)
    replaced_spaces = replace_spaces(removed_spaces)
    return replaced_spaces