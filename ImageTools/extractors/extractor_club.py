from config import logger
from utils.image_utils import take_and_use_screenshot, capture_screenshot, remove_screenshot, resize_image_path
from utils.text_utils import remove_newlines, remove_excessive_spaces, replace_spaces
from game.clubs.club_cleaner import (
    clean_extracted_club_name,
    fix_short_data,
    fix_extracted_data,
    weight_to_team,
    has_req_met
)
from ImageTools.extractors.extractor_base import crop_and_read_category, crop_and_read_image
from ImageTools.croppers.crop_base import use_cropped_image, crop_image, resize_and_crop_from_path


def read_club_names() -> list[str]:
    club_names = []
    # Extract Club names
    # with take_and_use_screenshot() as screenshot:
    screenshot = capture_screenshot()
    extracted_names = crop_and_read_category(screenshot, "club_names")
    remove_screenshot(screenshot)
    # clean extracted names
    for name in extracted_names.values():
        cleaned_club_name = clean_extracted_club_name(name)
        club_names.append(cleaned_club_name)
    return club_names


def extract_necessary_club_info_in_event() -> dict:
    # with take_and_use_screenshot() as screenshot:
    screenshot_path = capture_screenshot()
    extracted_data = crop_and_read_category(screenshot_path, "in_event_club_info")
    fixed_data = fix_short_data(extracted_data)
    req_list = get_req_list(fixed_data)
    logger.debug(f"req_list: {req_list}")
    fixed_data["req_list"] = req_list
    remove_screenshot(screenshot_path)
    return fixed_data


def extract_club_info() -> dict:
    # with take_and_use_screenshot() as screenshot:
    screenshot_path = capture_screenshot()
    # Extract Club info
    extracted_data = crop_and_read_category(screenshot_path, "club_info")
    # clean extracted data
    fixed_data = fix_extracted_data(extracted_data)
    # Get Weight Team
    weight_image =resize_and_crop_from_path(screenshot_path, "club_info", "weight")
    fixed_data['weight_team'] = weight_to_team(weight_image)
    weight_image.close()
    
    req_met_list = []
    for i in range(1, 3):
        req_image = resize_and_crop_from_path(screenshot_path, "club_info", f"reqs{i}")
        req_met = has_req_met(req_image)
        req_met_list.append(req_met)
        req_image.close()
        
    if 'NOT_MET' in req_met_list:
        fixed_data['req_status'] = 'NOT_MET'
    else:
        fixed_data['req_status'] = 'MET'
    
    remove_screenshot(screenshot_path)
    faults = get_faulty_club_info_data(fixed_data)
    if faults:
        fixed_data = fix_club_info(fixed_data, faults)
        
    #AddedReq_list
    fixed_data['req_list'] = get_req_list(fixed_data)
    return fixed_data
        
def get_req_list(extracted_data) -> list:
    req1_number = int(extracted_data["reqs1"]["number"])
    req2_number = int(extracted_data["reqs2"]["number"])
    req_list = [req1_number, req2_number]
    return req_list


def get_faulty_club_info_data(extracted_data):
    faults = []
    if extracted_data['score_left'] == 'None':
        faults.append('score_left')
    if extracted_data['score_right'] == 'None':
        faults.append('score_right')
    if extracted_data['weight'] == 'None':
        faults.append('weight')
    if extracted_data['reqs1']['name'] == 'NONE':
        faults.append('reqs1')
    if extracted_data['reqs2']['name'] == 'NONE':
        faults.append('reqs2')
    return faults

def fix_club_info(extracted_data, faults):
    counter = 0
    default_dict = {'score_left': '8000', 'score_right': '8000', 'weight': '100'}
    while faults:
        screenshot = capture_screenshot()
        for fault in faults:
            new_value = crop_and_read_image(screenshot, 'club_info', fault)
            extracted_data[fault] = new_value
        remove_screenshot(screenshot)

        extracted_data = fix_extracted_data(extracted_data)
        faults = get_faulty_club_info_data(extracted_data)
        counter += 1
        if counter > 3:
            for fault in faults:
                extracted_data[fault] = default_dict[fault]
            break
    return extracted_data



def evaluate_club_pick():
    extracted_data = extract_club_info()
    logger.debug(f"extracted_data, Req_status: {extracted_data['req_status']}")
    if extracted_data['req_status'] == 'NOT_MET':
        return None, None
    
    pickscore = 0
    
    left_score = int(extracted_data['score_left'])
    right_score = int(extracted_data['score_right'])
    weight = int(extracted_data['weight'])
    name = extracted_data['name']
    left_team = name.split(' ')[0]
    weight_team = extracted_data['weight_team']
    
    # WINNING TEAM_SIDE
    left_winning = False
    if left_team == weight_team:
        left_winning = True
    

    if left_score + right_score < 5000:
            pickscore = 1

    if left_score < 4000 and left_winning:
        pickscore = 2
    elif right_score < 4000 and not left_winning:
        pickscore = 2
    if weight > 1000:
        pickscore = 3
    if left_winning and weight > 300 and left_score < 6000:
        pickscore = 4
    if not left_winning and weight > 300 and right_score < 6000:
        pickscore = 4
    if left_score < 4000 or right_score < 4000:
        pickscore = 5
        
        
    if pickscore == 0:
        pickscore = (left_score + right_score) // 2
        
    # TODO: MYSIDE ADDING

    logger.debug(f"pickscore: {pickscore}")
    
    return pickscore, extracted_data
