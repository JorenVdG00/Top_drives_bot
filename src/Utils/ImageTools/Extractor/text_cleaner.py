import re
import os
from logging import Logger

from src.Utils.ImageTools.image_utils import ColorUtils
# from src.TopDrives.base_bot import BotBase
class TextCleaner():
    def __init__(self, bot_base: 'BotBase'):
        self.bot = bot_base
    
        
    @staticmethod
    def remove_newline(input_string):
        return input_string.split('\n')[0]

    @staticmethod
    def remove_excessive_spaces(input_string):
        # This regex replaces multiple spaces between words with a single space
        # and removes trailing spaces at the end of the string
        return re.sub(r'\s+', ' ', input_string).strip()

    @staticmethod
    def replace_spaces(input_string):
        return input_string.replace(' ', '_')

    @staticmethod
    def delete_last_char(input_string):
        return input_string[-1]

    @staticmethod
    def extract_integers(s):
        # Find all digits in the string
        digit_strings = re.findall(r'\d', s)
        if digit_strings:
            # Join them together and convert to a single integer
            combined_integer = int(''.join(digit_strings))
            return combined_integer
        return None

    @staticmethod
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

class ClubCleaner(TextCleaner):
    def __init__(self, bot_base: 'BotBase'):
        super().__init__(bot_base=bot_base)
        self.color_utils = ColorUtils(self.bot.logger)
        self.team_colors = {'FULL_THROTTLE': (203, 119, 86, 255),
                            'LEGACY': (255, 247, 177, 255),
                            'MIDNIGHT': (74, 136, 163, 255)}

    def weight_to_team(self, image):
        for color, color_code in self.team_colors.items():
            if self.color_utils.contains_color(image, color_code):
                return color
        print("something went wrong")
        return None

    def correct_weight_value(self, s):
        value = self.extract_integers(s)
        if value is None:
            return 5
        if len(str(value)) > 1:
            fixed_value = str(value)[1:]
        else:
            fixed_value = str(value)
        return int(fixed_value)

    def fix_rq_value(self, string):
        rq_value = string
        correct_rq = self.extract_integers(rq_value)
        return correct_rq

    def fix_score_value(self, extracted_data):
        left_score = extracted_data['score-left']
        right_score = extracted_data['score-right']
        extracted_data['score-left'] = self.extract_integers(left_score)
        extracted_data['score-right'] = self.extract_integers(right_score)
        return extracted_data

    def fix_reqs(self, extracted_data):
        for i in range(1, 3):
            req_str = extracted_data[f'reqs{i}_coords']
            cutted_str = self.cut_until_integer(req_str)
            req_split = cutted_str.rsplit(' ', 1)
            req_name, req_number = req_split[0], req_split[1][-1]
            if req_number is None:
                req_number = 0
            extracted_data[f'reqs{i}_coords'] = {'name': req_name, 'number': req_number}
        return extracted_data

    def has_req_met(self, image):
        reqs_met_color = (0, 244, 0, 255)
        reqs_not_met_color = (117, 123, 135, 255)
        if self.color_utils.contains_color(image, reqs_met_color, tolerance=10):
            return 'MET'
        elif self.color_utils.contains_color(image, reqs_not_met_color, tolerance=10):
            return 'NOT_MET'
        else:
            return 'NONE'



    def fix_players(self, extracted_data):
        side_list = ['left', 'right']
        for side in side_list:
            xamount = extracted_data[f'players_{side}'].replace(" ", "")
            if '/150' in xamount:
                extracted_data[f'players_{side}'] = xamount.split('/')[0]
                continue
            amount = self.cut_until_integer(xamount)
            if len(amount) == 0:
                extracted_data[f'players_{side}'] = 10
        return extracted_data

    def fix_extracted_data(self, extracted_data):

        # fix player_amounts
        extracted_data = self.fix_players(extracted_data)

        # fix requirements
        extracted_data = self.fix_reqs(extracted_data)

        # fix scores
        extracted_data = self.fix_score_value(extracted_data)

        # fix rq
        extracted_data['rq'] = self.fix_rq_value(extracted_data['rq'])
        # fix weight value because it add a number too much
        extracted_data['weight'] = self.correct_weight_value(extracted_data['weight'])

        return extracted_data
