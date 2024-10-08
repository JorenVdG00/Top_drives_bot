from src.Utils.ImageTools.Extractor.extractor_base import ExtractorBase
from src.Utils.ImageTools.Extractor.text_cleaner import ClubCleaner


class ExtractorClub(ExtractorBase):
    def __init__(self, bot_base):
        super().__init__(bot_base=bot_base)
        self.club_dict = None
        self.cleaner = ClubCleaner(bot_base)

    def read_club_names(self) -> list:
        club_names = []

        with self.image_utils.take_and_use_screenshot as image:
            extracted_names = self.crop_and_read_category('club_names')
        for key, value in extracted_names.items():
            cleaned_name = self.cleaner.remove_newline(value)
            removed_spaces = self.cleaner.remove_excessive_spaces(cleaned_name)
            no_spaces = self.cleaner.replace_spaces(removed_spaces)
            club_names.append(no_spaces)
        return club_names

    def extract_club_info(self) -> dict:
        with self.image_utils.take_and_use_screenshot as image:
            extracted_club_info = self.crop_and_read_category(image, 'club_info')
            extracted_data = self.cleaner.fix_extracted_data(extracted_club_info)

            with self.cropper.use_cropped_image(image, 'club_info', 'weight') as weight_image:
                weight_color = self.cleaner.weight_to_team(weight_image)
            extracted_data['weight_team'] = weight_color

            req_met_list = []
            for i in range(1, 3):
                with self.cropper.use_cropped_image(image, 'club_info', f'reqs{i}_coords') as req_image:
                    req_met = self.cleaner.has_req_met(req_image)
                    req_met_list.append(req_met)

            if 'NOT_MET' in req_met_list:
                extracted_data['req_status'] = 'NOT_MET'
            else:
                extracted_data['req_status'] = 'MET'
        self.club_dict = extracted_data
        return extracted_data

    def evaluate_club_pick(self):
        extracted_data = self.extract_club_info()

        # NOTS
        if self.club_dict['req_status'] == 'NOT_MET':
            return None

        left_score = int(self.club_dict['left_score'])
        right_score = int(self.club_dict['right_score'])
        weight = int(self.club_dict['weight'])
        name = self.club_dict['name']
        left_team = name.split(' ')[0]
        weight_team = self.club_dict['weight_team']

        left_winning = False
        if left_team == weight_team:
            left_winning = True

        if left_score + right_score < 5000:
            return 1

        if left_score < 4000 and left_winning:
            return 2
        elif right_score < 4000 and not left_winning:
            return 2
        if weight > 1000:
            return 3
        if left_winning and weight > 500 and left_score < 6000:
            return 4
        if not left_winning and weight > 500 and right_score < 6000:
            return 4

        pickscore = (left_score + right_score) // 2
        return pickscore, extracted_data

        # TODO: MYSIDE ADDING

    def get_req_list(self) -> list:
        req1_number = int(self.club_dict['reqs1_coords']['number'])
        req2_number = int(self.club_dict['reqs2_coords']['number'])
        req_list = [req1_number, req2_number]
        return req_list
