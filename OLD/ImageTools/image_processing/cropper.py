from PIL import Image
from OLD.Utils.image_utils import resize_image
from OLD.Utils.file_utils import create_dir_if_not_exists
from OLD.ImageTools import STANDARD_SIZE

def crop_image(image_path, save_dir, name, coords, standard_size=STANDARD_SIZE):
    with Image.open(image_path) as img:
        resized_image = resize_image(img, standard_size)
        cropped_image = resized_image.crop(coords)
        create_dir_if_not_exists(save_dir)
        save_path = f"{save_dir}/{name}.png"
        cropped_image.save(save_path)
    return save_path

def crop_image_no_save(image_path, coords, standard_size=STANDARD_SIZE):
    with Image.open(image_path) as img:
        resized_image = resize_image(img, standard_size)
        cropped_image = resized_image.crop(coords)
        return cropped_image