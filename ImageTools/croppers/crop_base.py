import os
from PIL import Image
from contextlib import contextmanager
from utils.coords_utils import CoordsUtils, logger
from utils.image_utils import resize_image, resize_image_path

COORDSUTILS = CoordsUtils()
def crop_image(image: Image, category:str, sub_cat:str) -> Image:
    """
    Crop an image based on the provided category and subcategory.

    Args:
        image (Image): The image to crop.
        category (str): The category of the coords.
        sub_cat (str): The subcategory of the coords to crop the image.

    Returns:
        Image: A cropped image if the category and subcategory are found in the coords yml file; otherwise, None.
    """
    coords = COORDSUTILS.get_crop_coords(category, sub_cat)
    if coords:
        logger.debug(f'Coords = {coords}')
        coords = COORDSUTILS.coords_str_to_tuple(coords)
        cropped_image = image.crop(coords)
        return cropped_image
    else:
        return None

def crop_all_types(image: Image, category: str, save_dir:str) -> dict[str, str]:
    """
    Crop an image into all types of a given category and save them.

    Args:
        image (Image): The image to crop.
        category (str): The category of the coords.
        save_dir (str): The directory to save the cropped images.

    Returns:
        dict[str, str]: A dictionary of cropped images with the keys as the name of the cropped image and the value as the path to the saved image.
    """
    resized_image = resize_image(image)
    coords_dict = COORDSUTILS.get_crop_dict(category)
    if coords_dict is None:
        logger.error(f"No coords found for category: {category}")
        return None
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
            logger.debug(f'Cropped image {key} saved to {save_path}')
    return img_dict

@contextmanager
def use_cropped_image(image: Image, category: str, sub_cat: str):
    """
    Context manager for capturing and automatically removing a cropped image.
    """
    cropped_image = crop_image(image, category, sub_cat)
    
    # Check if the cropping operation was successful
    if cropped_image is None:
        logger.error("Cropping failed, cropped_image is None")
        yield None  # Yield None so the caller knows the operation failed
    else:
        try:
            yield cropped_image
        except Exception as e:
            logger.error(f"Error while using cropped image: {e}")
        finally:
            try:
                cropped_image.close()  # Only close if it's not None
            except AttributeError:
                logger.error("Error closing cropped image: Image was None")
                
                
def resize_and_crop_from_path(image_path: str, category: str, sub_cat: str) -> str:
    resized_image = resize_image_path(image_path)
    cropped_image = crop_image(resized_image, category, sub_cat)
    return cropped_image