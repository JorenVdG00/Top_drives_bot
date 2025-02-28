from ImageTools import pytesseract
from ImageTools.croppers.crop_base import use_cropped_image, COORDSUTILS, crop_image
from app.utils.ImageTools.image_utils import resize_image, open_image, close_image
from PIL import Image


def extract_text(image: Image) -> str:
    """
    Extracts text from an image using Tesseract OCR.

    Args:
        image (Image): The image to extract text from.

    Returns:
        str: The extracted text.
    """
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text


def crop_and_read_image(image_path: str, category: str, sub_cat: str) -> str:
    """
    Crop and read an image based on the provided category and subcategory.

    Args:
        image (Image): The image to crop and read.
        category (str): The category of the coordinates.
        sub_cat (str): The subcategory of the coordinates to crop and read the image.

    Returns:
        str: The extracted text from the cropped image.
    """
    # Open original image
    image = open_image(image_path)
    # Resize original image and keep resized image
    resized_img = resize_image(image)
    close_image(image)
    
    cropped_image = crop_image(resized_img, category, sub_cat)
    close_image(resized_img)
    
    extracted_text = extract_text(cropped_image)
    close_image(cropped_image)
    return extracted_text
    
    with use_cropped_image(resized_img, category, sub_cat) as image_cropped:
        extracted_text = extract_text(image_cropped)
        return extracted_text


def crop_and_read_category(image_path: str, category: str):
    extract_dict = {}
    crop_dict = COORDSUTILS.get_crop_dict(category)
    for key, val in crop_dict.items():
        if key == "category":
            continue
        if isinstance(val, dict):
            for sub_cat in val:
                extract_dict[sub_cat] = crop_and_read_image(
                    image_path, category, sub_cat
                )
        else:
            extract_dict[key] = crop_and_read_image(image_path, category, key)
    return extract_dict



#TODO: MOVE TO CHECKER
#? NOT HERE
#! ################################################################################
def crop_and_check_color(
    self, image: Image, category: str, sub_cat: str, color: str
):
    with self.cropper.use_cropped_image(image, category, sub_cat) as cropped_image:
        return self.bot.image_utils.color_utils.contains_color(
            cropped_image, color, 5
        )