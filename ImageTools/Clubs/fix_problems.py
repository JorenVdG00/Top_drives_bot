from PIL import Image
from ImageTools.utils.image_utils import color_almost_matches, resize_image
from ImageTools.image_processing.cropper import crop_image_no_save
from ImageTools.image_processing.extractor import extract_text_from_image
from UI.functions.general_functions import capture_screenshot,remove_screenshot
import os



def check_problem():
    screenshot = capture_screenshot()
    x,y = (1450, 750)
    coords = (110, 450, 2100, 690)
    problem_color = (51,51,51,255)
    with Image.open(screenshot) as img:
        resised_img = resize_image(img)
        color = resised_img.getpixel((x, y))
        if not color_almost_matches(color, problem_color):
            status = 'NO_PROBLEM'
    cropped_img = crop_image_no_save(screenshot, coords)
    extracted_text = extract_text_from_image(cropped_img)
    print(extracted_text)
    remove_screenshot(screenshot)
    if status == 'NO_PROBLEM':
        return status
    if 'ended' in extracted_text:
        return 'EVENT_ENDED'
    elif 'servicing' in extracted_text:
        return 'CARS_REPAIR'
    else:
        return 'OTHER'


def get_car_with_repairs():
    screenshot = capture_screenshot()
    y = 1080
    x_start = 230
    x_step = 350
    repair_color = (255, 76, 76, 255)
    need_repair = []
    with Image.open(screenshot) as img:
        resized_img = resize_image(img)
        for i in range(5):
            x = x_start + (i * x_step)
            color = resized_img.getpixel((x, y))
            if color_almost_matches(color, repair_color):
                need_repair.append(i+1)
    remove_screenshot(screenshot)
    return need_repair