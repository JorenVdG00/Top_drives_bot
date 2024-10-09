import os

from PIL import Image
from contextlib import contextmanager
# from src.TopDrives.base_bot import BotBase


class CropperBase():
    def __init__(self, bot_base: 'BotBase'):
        self.bot = bot_base
        self.crop_map = {}
        self.logger = self.bot.logger
        self._initialize_crop_map()

    def crop_image(self, image, category, sub_cat) -> Image:
        coords = self.bot.file_utils.get_crop_coords(category, sub_cat)
        if coords:
            print(f'Coords = {coords}')
            coords = self.bot.file_utils.coords_str_to_tuple(coords)
            cropped_image = image.crop(coords)
            return cropped_image
        else:
            return None


    def crop_all_types(self, image, category, save_dir):
        resized_image = self.bot.resizer.resize_img(image)
        coords_dict = self.bot.file_utils.get_crop_dict(category)
        img_dict = {}
        for key, value in coords_dict.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    cropped_image = resized_image.crop(sub_value)
                    save_path = os.path.join(save_dir, f'{key}-{sub_key}.png')
                    img_dict[sub_key] = save_path
                    cropped_image.save(save_path)
            else:
                save_path = os.path.join(save_dir, f'{key}.png')
                img_dict[key] = save_path
                cropped_image = resized_image.crop(value)
                cropped_image.save(save_path)
        return img_dict

    def crop_image_with_subtitle(self, image, title, sub_title) -> Image:
        title = self.crop_map.get(title)
        if title is None:
            self.logger.error(f"No coordinates found for action: {title}")
            return None
        cropped_image = self.crop_image(image, title, sub_title)
        return cropped_image

    def crop_category(self, image: Image, title: str, save_dir) -> dict | bool:
        title = self.crop_map.get(title)
        if title is None:
            self.logger.error(f"No coordinates found for action: {title}")
            return False
        if save_dir:
            img_dict = self.crop_all_types(image, title, save_dir)
            return img_dict

    def _initialize_crop_map(self):
        """
        Initialize and update the check_map with predefined checks.
        This method is intended to be called during the object initialization
        to populate the check_map with common checks.
        """
        base_crops = {
            'go_button_problem': 'go_button_problem',
            'club_info_coords': 'club_info_coords',
        }
        self.crop_map.update(base_crops)

    
    @contextmanager
    def use_cropped_image(self, image: Image, category: str, sub_cat: str):
        """
        Context manager for capturing and automatically removing a cropped image.
        """
        cropped_image = self.crop_image(image, category, sub_cat)
        
        # Check if the cropping operation was successful
        if cropped_image is None:
            self.logger.error("Cropping failed, cropped_image is None")
            yield None  # Yield None so the caller knows the operation failed
        else:
            try:
                yield cropped_image
            except Exception as e:
                self.logger.error(f"Error while using cropped image: {e}")
            finally:
                try:
                    cropped_image.close()  # Only close if it's not None
                except AttributeError:
                    self.logger.error("Error closing cropped image: Image was None")