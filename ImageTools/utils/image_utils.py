import math
from PIL import Image


def resize_image(image, standard_size=(2210, 1248)):
    return image.resize(standard_size, Image.Resampling.LANCZOS)

def contains_color(image_path, target_rgb, tolerance=5):
    image = Image.open(image_path)
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if color_distance(pixels[x, y], target_rgb) <= tolerance:
                return True
    return False


def color_distance(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1[:3], c2[:3])))  # Ignore the alpha channel


def check_consecutive_pixels(image_path, filter_color, tolerance=10, required_consecutive=30, horizontal=True):
    image = Image.open(image_path).convert('RGBA')
    if horizontal:
        width, height = image.size
    else:
        # swapped so looks at vertical alignment
        height, width = image.size
    for y in range(height):
        consecutive_count = 0
        for x in range(width):
            pixel_color = image.getpixel((x, y))
            if color_distance(pixel_color, filter_color) <= tolerance:
                consecutive_count += 1
                if consecutive_count >= required_consecutive:
                    return True
            else:
                consecutive_count = 0
    return False
