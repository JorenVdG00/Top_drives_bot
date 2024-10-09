# from src.TopDrives.base_bot import BotBase
from src.Utils.ImageTools.Cropper.cropper_base import CropperBase
from src.Utils.ImageTools import pytesseract
from src.Utils.ImageTools.Extractor.text_cleaner import TextCleaner
from PIL import Image


class ExtractorBase:
    def __init__(self, bot_base: "BotBase"):
        self.bot = bot_base
        self.logger = self.bot.logger
        self.cropper = CropperBase(bot_base)
        self.cleaner = TextCleaner(bot_base)

    def crop_and_read_image(self, image: Image, category: str, sub_cat: str):
        resized_img = self.bot.resizer.resize_img(image)
        with self.cropper.use_cropped_image(
            resized_img, category, sub_cat
        ) as image_cropped:
            extracted_text = self.extract_text(image_cropped)
            return extracted_text

    def crop_and_read_category(self, image: Image, category: str):
        extract_dict = {}
        crop_dict = self.bot.file_utils.get_crop_dict(category)
        for key, val in crop_dict.items():
            if key == "category":
                continue
            if isinstance(val, dict):
                for sub_cat in val:
                    extract_dict[sub_cat] = self.crop_and_read_image(
                        image, category, sub_cat
                    )
            else:
                extract_dict[key] = self.crop_and_read_image(image, category, key)
        return extract_dict

    def crop_and_check_color(
        self, image: Image, category: str, sub_cat: str, color: str
    ):
        with self.cropper.use_cropped_image(image, category, sub_cat) as cropped_image:
            return self.bot.image_utils.color_utils.contains_color(
                cropped_image, color, 5
            )

    @staticmethod
    def extract_text(image: Image) -> str:
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text
