import math
import os
from datetime import datetime
from PIL import Image
from contextlib import contextmanager
from config import BOT_SCREENSHOTS_DIR, ADB_SERIAL_CMD, logger
# from functions.general_functions import capture_screenshot, remove_screenshot
from utils.os_utils import set_cwd, create_dir_if_not_exists
from typing import Optional




def open_image(image_path):
    # if isinstance(image_path, Image.Image):
    #     # If already an image object, return it directly
    #     return image_path
    return Image.open(image_path)

def close_image(image: Image):
    image.close()

@contextmanager
def screenshot_context():
    screenshot = capture_screenshot()
    try:
        yield screenshot
    finally:
        remove_screenshot(screenshot)

@contextmanager
def take_and_use_screenshot():
    """Context manager to take a screenshot and open it as a PIL Image.

    The screenshot is automatically removed when the context manager is exited.

    Yields:
        A PIL Image object representing the screenshot.
    """
    screenshot = capture_screenshot()

    try:
        image = Image.open(screenshot)  # Open the image
        yield image  # Yield the image without auto-closing
    finally:
        image.close()  # Ensure it is closed only when we're done
        remove_screenshot(screenshot)  # Clean up the file

def resize_image(image: Image, standard_size=(2210, 1248)) -> Image:
    """
    Resizes the input image to the specified standard size using Lanczos resampling.

    Args:
        image: The input image to be resized.
        standard_size: The desired size to resize the image to. Default is (2210, 1248).

    Returns:
        Image: The resized image.
    """
    return image.resize(standard_size, Image.Resampling.LANCZOS)

def resize_image_path(image_path, standard_size=(2210, 1248)):
    with Image.open(image_path) as image:
        resized_image = resize_image(image, standard_size)
        return resized_image

def get_resized_image(screenshot: Optional[str] = None):
    """
    Helper method to get a resized image from either a provided screenshot or the current screen.

    Args:
        screenshot (Optional[str]): The path to a screenshot file.

    Returns:
        Image: Resized image.
    """
    if screenshot:
        if isinstance(screenshot, Image.Image):
            resized_img = resize_image(screenshot)
        else:
            resized_img = resize_image_path(screenshot)

    else:
        with take_and_use_screenshot() as screenshot_img:
            resized_img = resize_image(screenshot_img)
    return resized_img


def contains_color(image: Image, color: tuple[int, int, int, int], tolerance: int = 5):
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if color_distance(pixels[x, y], color) <= tolerance:
                logger.debug(f'Color {color} found in pixels {x}, {y}')
                return True
    return False

def color_almost_matches(color, target_rgb, tolerance=10):

    return color_distance(color, target_rgb) <= tolerance


def color_distance(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1[:3], c2[:3])))  # Ignore the alpha channel


def check_consecutive_pixels(image: Image, target_color, tolerance=10, required_consecutive=30,
                                 horizontal=True):
    if horizontal:
        width, height = image.size
    else:
        # swapped so looks at vertical alignment
        height, width = image.size
    for y in range(height):
        consecutive_count = 0
        for x in range(width):
            pixel_color = image.getpixel((x, y))
            if color_distance(pixel_color, target_color) <= tolerance:
                consecutive_count += 1
                if consecutive_count >= required_consecutive:
                    logger.debug(f'Consecutive pixels found in image {x}, {y}')
                    return True
            else:
                consecutive_count = 0
    return False

def capture_screenshot(parent_dir=None, sub_dir=None, name=None):
    set_cwd()
    enough_args = False
    if parent_dir is None or sub_dir is None or name is None:
        enough_args = False
    else:
        enough_args = True
        create_dir_if_not_exists(parent_dir, sub_dir)
    if not enough_args:
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        # Construct the screenshot filename
        filename = f"{BOT_SCREENSHOTS_DIR}/screenshot_{timestamp}.png"
    else:
        filename = f"{parent_dir}/{sub_dir}/{name}.png"
    # Take the screenshot
    os.system(f"{ADB_SERIAL_CMD} shell screencap -p /sdcard/screenshot.png")
    os.system(f"{ADB_SERIAL_CMD} pull /sdcard/screenshot.png " + filename)
    os.system(f"{ADB_SERIAL_CMD} shell rm /sdcard/screenshot.png")
    print(f"Screenshot saved to {filename}")
    return filename


def remove_screenshot(filename):
    os.remove(filename)
    
def check_color_at_location(image: Image, coords: tuple[int, int],
                            target_color: tuple[int, int, int, int], tolerance: int = 10) -> bool:
    color = image.getpixel(coords)
    if color_almost_matches(color, target_color, tolerance):
        return True
    else:
        return False

def get_color_at_location(image: Image, coords: tuple[int,int]) -> tuple[int,int,int,int]:
    return image.getpixel(coords)


