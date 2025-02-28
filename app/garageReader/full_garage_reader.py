from app.utils.ImageTools.image_utils import capture_screenshot
from game.general.general_actions import swipe_left_cars, tap_home, tap_all_cars
from game.general.general_checks import get_nr_available_cars
from garageReader.garage_cropper import get_start_and_crop_first_four
from garageReader.garage_reader import extract_car_info
from scraper.car_scraper import scrape_all_cars

import time


def capture_all_cars():
    """
    Captures all cars in garage and crops them, returning a list of their paths
    """
    
    cropped_cars_img_dirs = []
    tap_home()
    time.sleep(0.5)
    tap_all_cars()
    
    screenshot = capture_screenshot()
    while get_nr_available_cars(screenshot)>0:
        screenshot = capture_screenshot() # before because getnr sometimes 0 when there is 2 more
        cropped_cars_img_dirs.extend(get_start_and_crop_first_four(screenshot, len(cropped_cars_img_dirs)))
        swipe_left_cars()
    return cropped_cars_img_dirs
    

def get_all_cars(cars_img_dirs):
    cars_dict = {}
    faulty_NRs = []
    for index, car_dir in enumerate(cars_img_dirs):
        car = extract_car_info(car_dir)
        if car['brand'] != None:
            cars_dict[index] = car
        else:
            faulty_NRs.extend(index)

    found_cars, faulty_cars = scrape_all_cars(cars_dict)
    faulty_NRs.extend(faulty_cars)
    
    return found_cars, faulty_NRs


