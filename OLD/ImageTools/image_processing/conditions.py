from OLD.Utils.image_utils import contains_color, check_consecutive_pixels

condition_colors = {
    'SUN': (255, 232, 147, 255),
    'HIGH': (255, 114, 85, 255),
    'WET': (109, 208, 247, 255)
}


def get_conditions(image_path):
    condition_dict = {}
    for condition, color_code in condition_colors.items():
        if condition == 'HIGH':
            if contains_color(image_path, color_code):
                if check_consecutive_pixels(image_path, color_code, required_consecutive=30):
                    condition_dict['HIGH'] = True
                    condition_dict['ROLLING'] = False
                else:
                    condition_dict['ROLLING'] = True
                    condition_dict['HIGH'] = False
        else:
            condition_dict[condition] = contains_color(image_path, color_code)
    return condition_dict
