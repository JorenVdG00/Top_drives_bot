from src.Utils.ImageTools.Extractor.extractor_base import ExtractorBase
from src.Utils.ImageTools.Extractor.text_cleaner import ClubCleaner


class ExtractorClub(ExtractorBase):
    def __init__(self, bot_base):
        super().__init__(bot_base=bot_base)
        self.club_dict = None
        self.cleaner = ClubCleaner(bot_base)
        self.image_utils = bot_base.image_utils

    def read_club_names(self) -> list:
        club_names = []

        with self.image_utils.take_and_use_screenshot as image:
            extracted_names = self.crop_and_read_category(image, 'club_names')
        for key, value in extracted_names.items():
            cleaned_name = self.cleaner.remove_newline(value)
            removed_spaces = self.cleaner.remove_excessive_spaces(cleaned_name)
            no_spaces = self.cleaner.replace_spaces(removed_spaces)
            club_names.append(no_spaces)
        return club_names

    def extract_necessary_club_info_in_event(self) -> dict:
        with self.image_utils.take_and_use_screenshot() as image:
            extracted_club_info = self.crop_and_read_category(image, 'in_event_club_info')
            fixed_data = self.cleaner.fix_short_data(extracted_club_info)
            req_list = self.get_req_list(fixed_data)
            fixed_data['req_list'] = req_list
        return fixed_data
    
    def extract_club_info(self) -> dict:
        with self.image_utils.take_and_use_screenshot() as image:
            extracted_club_info = self.crop_and_read_category(image, 'club_info')
            for index, (key, value) in enumerate(extracted_club_info.items()):
                print(index, key, value)
            extracted_data = self.cleaner.fix_extracted_data(extracted_club_info)
            
            with self.cropper.use_cropped_image(image, 'club_info', 'weight') as weight_image:
                weight_color = self.cleaner.weight_to_team(weight_image)
            extracted_data['weight_team'] = weight_color

            req_met_list = []
            for i in range(1, 3):
                with self.cropper.use_cropped_image(image, 'club_info', f'reqs{i}') as req_image:
                    req_met = self.cleaner.has_req_met(req_image)
                    req_met_list.append(req_met)

            if 'NOT_MET' in req_met_list:
                extracted_data['req_status'] = 'NOT_MET'
            else:
                extracted_data['req_status'] = 'MET'
            
        faults = self.get_faulty_club_info_data(extracted_data)
        if faults:
            extracted_data = self.fix_club_info(extracted_data, faults)                
            
        self.club_dict = extracted_data
        return extracted_data

    def evaluate_club_pick(self):
        extracted_data = self.extract_club_info()

        # NOTS
        if extracted_data['req_status'] == 'NOT_MET':
            return None

        left_score = int(extracted_data['score_left'])
        right_score = int(extracted_data['score_right'])
        weight = int(extracted_data['weight'])
        name = extracted_data['name']
        left_team = name.split(' ')[0]
        weight_team = extracted_data['weight_team']

        left_winning = False
        if left_team == weight_team:
            left_winning = True
            
        pickscore = 0

        if left_score + right_score < 5000:
            pickscore = 1

        if left_score < 4000 and left_winning:
            pickscore = 2
        elif right_score < 4000 and not left_winning:
            pickscore = 2
        if weight > 1000:
            pickscore = 3
        if left_winning and weight > 500 and left_score < 6000:
            pickscore = 4
        if not left_winning and weight > 500 and right_score < 6000:
            pickscore = 4
        if left_score < 2500 or right_score < 2500:
            pickscore = 5
        if pickscore == 0:
            pickscore = (left_score + right_score) // 2
        return pickscore, extracted_data

        # TODO: MYSIDE ADDING

    def get_req_list(self, extracted_data) -> list:
        req1_number = int(extracted_data['reqs1']['number'])
        req2_number = int(extracted_data['reqs2']['number'])
        req_list = [req1_number, req2_number]
        return req_list


    def get_faulty_club_info_data(self, extracted_data):
        faults = []
        if extracted_data['score_left'] == 'None':
            faults.append('score_left')
        if extracted_data['score_right'] == 'None':
            faults.append('score_right')
        if extracted_data['weight'] == 'None':
            faults.append('weight')
        return faults
    
    def fix_club_info(self, extracted_data, faults):
        counter = 0
        default_dict = {'score_left': '8000', 'score_right': '8000', 'weight': '100'}
        while faults:
            with self.image_utils.take_and_use_screenshot() as image:
                for fault in faults:
                    new_value = self.crop_and_read_image(image, 'club_info', fault)
                    extracted_data[fault] = new_value

            extracted_data = self.cleaner.fix_extracted_data(extracted_data)
            faults = self.get_faulty_club_info_data(extracted_data)
            counter += 1
            if counter > 3:
                for fault in faults:
                    extracted_data[fault] = default_dict[fault]
                break
        return extracted_data