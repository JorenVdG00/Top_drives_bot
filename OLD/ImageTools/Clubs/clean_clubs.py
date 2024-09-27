import os
import re
from OLD.Utils.image_utils import contains_color
from OLD.Database.db_getters import get_club_reqs

# TEAM_COLORS
team_colors = {'FULL_THROTTLE': (203, 119, 86, 255),
               'LEGACY': (255, 247, 177, 255),
               'MIDNIGHT': (74, 136, 163, 255)}


# LEGACY == YELLOW
# FULL_THROTTLE == RED
# MIDNIGHT == BLUE

def weight_to_team(image_path):
    for color, color_code in team_colors.items():
        if contains_color(image_path, color_code):
            return color
    print("something went wrong")
    return None


def correct_weight_value(s):
    value = extract_integers(s)
    if value is None:
        return 5
    if len(str(value)) > 1:
        fixed_value = str(value)[1:]
    else:
        fixed_value = str(value)
    return int(fixed_value)


def fix_rq_value(str):
    rq_value = str
    correct_rq = extract_integers(rq_value)
    return correct_rq


def fix_score_value(extracted_data):
    left_score = extracted_data['score-left_x']
    right_score = extracted_data['score-right_x']
    extracted_data['score-left_x'] = extract_integers(left_score)
    extracted_data['score-right_x'] = extract_integers(right_score)
    return extracted_data




def fix_reqs(extracted_data, club_dir_path):
    extracted_data['req_status'] = 'NULL'

    db_reqs = get_club_reqs()
    for i in range(1, 3):
        req_img = os.path.join(club_dir_path, f'reqs{i}.png')
        has_req = has_req_met(req_img)
        extracted_data['req_status'] = has_req
        if has_req != 'NONE':
            req_str = extracted_data[f'reqs{i}']
            cutted_str = cut_until_integer(req_str)
            req_split = cutted_str.rsplit(' ', 1)
            req_name, req_number = req_split[0], req_split[1][-1]
            print(req_name, req_number)
            extracted_data[f'reqs{i}'] = {'name': req_name, 'number': req_number}
            for db_req in db_reqs:
                if i == 1:
                    if db_req[0] in req_name:
                        extracted_data[f'reqs{i}']['name'], extracted_data[f'reqs{i}']['number'] = db_req[0], db_req[1]
                else:
                    if len(db_req) > 3 and db_req[2] in req_name:
                        extracted_data[f'reqs{i}']['name'], extracted_data[f'reqs{i}']['number'] = db_req[2], db_req[3]
        else:
            if extracted_data['req_status'] in ('NONE', 'MET'):
                extracted_data['req_status'] = 'MET'
            elif extracted_data['req_status'] == 'NOT_MET':
                extracted_data['req_status'] = 'NOT_MET'
    return extracted_data


def has_req_met(img_path):
    reqs_met_color = (0, 244, 0, 255)
    reqs_not_met_color = (117, 123, 135, 255)
    if contains_color(img_path, reqs_met_color, tolerance=10):
        return 'MET'
    elif contains_color(img_path, reqs_not_met_color, tolerance=10):
        return 'NOT_MET'
    else:
        return 'NONE'


def extract_integers(s):
    # Find all digits in the string
    digit_strings = re.findall(r'\d', s)
    if digit_strings:
        # Join them together and convert to a single integer
        combined_integer = int(''.join(digit_strings))
        return combined_integer
    return None

def cut_until_integer(s):
    index = len(s)

    # Iterate backward through the string
    for i in range(len(s) - 1, -1, -1):
        if s[i].isdigit():
            index = i
            break

    # Slice the string up to and including the first integer
    result = s[:index + 1]
    return result

def fix_players(extracted_data):
    print(extracted_data)
    side_list = ['left', 'right']
    for side in side_list:
        xamount = extracted_data[f'player_amount-{side}_x'].replace(" ", "")
        if '/150' in xamount:
            print(f'xamount == {xamount}')
            extracted_data[f'player_amount-{side}_x'] = xamount.split('/')[0]
            print(f'xamount == {extracted_data[f'player_amount-{side}_x']}')
            continue
        amount = cut_until_integer(xamount)
        if len(amount) == 0:
            extracted_data[f'player_amount-{side}_x'] = 10
    return extracted_data



def fix_extracted_data(extracted_data, club_dir_path):

    # fix player_amounts
    extracted_data = fix_players(extracted_data)

    # fix requirements
    extracted_data = fix_reqs(extracted_data, club_dir_path)

    #fix scores
    extracted_data = fix_score_value(extracted_data)

    #fix rq
    extracted_data['rq'] = fix_rq_value(extracted_data['rq'])
    # fix weight value because it add a number too much
    correct_weight = correct_weight_value(extracted_data['weight'])
    extracted_data['weight'] = correct_weight

    weight_img = os.path.join(club_dir_path, 'weight.png')
    weight_team = weight_to_team(weight_img)
    extracted_data['weight_team'] = weight_team

    return extracted_data



