import math
from logging import Logger
from contextlib import contextmanager

from PIL import Image, ImageEnhance, ImageFilter
from src.TopDrives.base_bot import ScreenshotManager

class ImageUtils:
    def __init__(self, logger: Logger, screen_manager: ScreenshotManager):
        self.logger = logger
        self.image = None
        self.color_utils = ColorUtils(self.logger)
        self.enhance = ImageEnhancements
        self.screen_manager = screen_manager

    def set_image(self, image: Image):
        self.image = image

    def save_image(self, image, image_path: str):
        image.save(image_path)

    @staticmethod
    def open_image(image_path: str) -> Image:
        image = Image.open(image_path)
        return image

    @staticmethod
    def close_image(image: Image):
        image.close()

    @contextmanager
    def take_and_use_screenshot(self):
        screenshot = self.screen_manager.capture_screenshot()

        try:
            with Image.open(screenshot) as image:
                yield image
        finally:
            self.screen_manager.remove_screenshot(screenshot)


class ColorUtils:
    def __init__(self, logger: Logger):
        self.logger = logger

    def check_color_at_location(self, image: Image, coords: tuple[int, int],
                                target_color: tuple[int, int, int, int]) -> bool:
        color = image.getpixel(coords)
        if self.color_almost_matches(color, target_color, 10):
            return True
        else:
            return False

    def contains_color(self, image: Image, color: tuple[int, int, int, int], tolerance: int = 5):
        pixels = image.load()
        for x in range(image.width):
            for y in range(image.height):
                if self.color_distance(pixels[x, y], color) <= tolerance:
                    self.logger.debug(f'Color {color} found in pixels {x}, {y}')
                    return True
        return False

    def color_almost_matches(self, color, target_color, tolerance=10):
        distance = self.color_distance(color, target_color)
        self.logger.debug(f'The color::{color}:: matches  :{distance}:  with ::{target_color}::')
        return distance <= tolerance

    def check_consecutive_pixels(self, image: Image, target_color, tolerance=10, required_consecutive=30,
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
                if self.color_distance(pixel_color, target_color) <= tolerance:
                    consecutive_count += 1
                    if consecutive_count >= required_consecutive:
                        self.logger.debug(f'Consecutive pixels found in image {x}, {y}')
                        return True
                else:
                    consecutive_count = 0
        return False

    @staticmethod
    def color_distance(color_1, color_2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(color_1[:3], color_2[:3])))  # Ignore the alpha channel


class ImageEnhancements:
    def __init__(self, image: Image):
        self.image = image

    def enhance_image(self, smoothen: bool = False, blur: bool = False, grayscale: bool = False,
                      binarize: bool = False, contrast: bool = False, sharpness: bool = False):
        if smoothen:
            self.smoothen_image()
        if blur:
            self.blur_image()
        if grayscale:
            self.convert_to_grayscale()
        if binarize:
            self.binarize_image()
        if contrast:
            self.enhance_contrast()
        if sharpness:
            self.enhance_sharpness()

    def enhance_contrast(self):
        enhancer = ImageEnhance.Contrast(self.image)
        enhanced_image = enhancer.enhance(2)  # Adjust factor as needed
        self.image = enhanced_image

    def convert_to_grayscale(self):
        self.image = self.image.convert('L')

    def binarize_image(self, threshold=128):
        grayscale_image = self.image.convert('L')
        self.image = grayscale_image.point(lambda p: p > threshold and 255)

    # def remove_noise(self):
    #     image = cv2.imread(image_path)
    #     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     denoised_image = cv2.fastNlMeansDenoising(gray_image, None, 30, 7, 21)
    #     cv2.imwrite(output_path, denoised_image)

    def smoothen_image(self):
        self.image = self.image.filter(ImageFilter.SMOOTH_MORE)

    def blur_image(self):
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius=2))

    def enhance_sharpness(self):
        enhancer = ImageEnhance.Sharpness(self.image)
        self.image = enhancer.enhance(2)


