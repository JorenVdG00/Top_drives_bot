from PIL import Image
import math
import os

image_path_1 = 'bot_screenshots/conditions/sun_rolling.png'
image_path_2 = 'bot_screenshots/conditions/high.png'

high_img_dir_path = 'bot_screenshots/conditions/HIGH'
rolling_img_dir_path = 'bot_screenshots/conditions/ROLLING'

filter_color = (255, 115, 85, 255)
tolerance = 10

def color_distance(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1[:3], c2[:3])))  # Ignore the alpha channel

def get_unique_colors(image1, image2, filter_color, tolerance):
    # Convert the images to sets of RGB tuples
    colors1 = set(image1.getdata())
    colors2 = set(image2.getdata())

    # Filter and find unique colors
    unique_to_image1 = [color for color in colors1 - colors2 if color_distance(color, filter_color) <= tolerance]
    unique_to_image2 = [color for color in colors2 - colors1 if color_distance(color, filter_color) <= tolerance]

    return unique_to_image1, unique_to_image2


# Function to get common colors in all images of a directory
def get_common_colors_in_dir(directory, filter_color, tolerance):
    common_colors = None

    for filename in os.listdir(directory):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(directory, filename)
            image = Image.open(image_path).convert('RGBA')
            colors = set([color for color in image.getdata() if color_distance(color, filter_color) <= tolerance])

            if common_colors is None:
                common_colors = colors
            else:
                common_colors &= colors  # Intersection to find common colors across all images

    return common_colors


# Function to find unique colors in one directory compared to another
def find_unique_colors_in_dirs(dir1, dir2, filter_color, tolerance):
    common_colors_dir1 = get_common_colors_in_dir(dir1, filter_color, tolerance)
    common_colors_dir2 = get_common_colors_in_dir(dir2, filter_color, tolerance)

    # Colors unique to dir1
    unique_to_dir1 = common_colors_dir1 - common_colors_dir2

    # Colors unique to dir2
    unique_to_dir2 = common_colors_dir2 - common_colors_dir1

    return unique_to_dir1, unique_to_dir2


# image1 = Image.open(image_path_1)
# cropped_image1 = image1.crop((155, 4, 250, 70))
# cropped_image1.show()
#
# image2 = Image.open(image_path_2)
# cropped_image2 = image2.crop((155, 4, 250, 70))
# cropped_image2.show()
#
# unique1, unique2 = get_unique_colors(cropped_image1, cropped_image2, filter_color, tolerance)
#
# print(unique1)
# print(unique2)

# pixel = image.getpixel((0, 0))
# print(pixel)

unique_colors_dir1, unique_colors_dir2 = find_unique_colors_in_dirs(high_img_dir_path, rolling_img_dir_path, filter_color, tolerance)
