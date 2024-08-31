import os

from UI.functions.general_functions import capture_screenshot, tap, swipe, remove_screenshot, create_dir_if_not_exists
from UI.functions.resize_functions import resize_coordinates, calculate_screen_size, set_cwd, resize_ranges
from UI.functions.event_functions import tap_event, tap_events, tap_home, check_event_available, tap_play_event
from image_reader.event.event_cropper_V3 import get_event_name, crop_and_save_event_type_images
from image_reader.event.event_reader_V2 import get_full_event_type_list
from image_reader.event.event_time import get_time_left_event, calculate_event_end_time
from database.db_general import add_event, add_series, add_race
from database.db_getters import get_event_id_by_name
from config import resize_values
import random
import time


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.join(BASE_DIR, 'temp')



def get_event_info():
    screenshot = capture_screenshot()
    event_name = get_event_name(screenshot)
    end_time = calculate_event_end_time(get_time_left_event(screenshot))
    # event_id = add_event(event_name, end_time)
    remove_screenshot(screenshot)
    return event_name, end_time


def tap_match_info():
    x1,x2,y1,y2 = resize_ranges(150, 630, 140, 210, resize_values)
    rand_x, rand_y = random.randint(x1, x2), random.randint(y1, y2)
    tap(rand_x, rand_y)
    time.sleep(1)

# def export_info_to_db(event_info):
#     ...

def full_event_reader():
    extract_data = {}

    calculate_screen_size()
    print(os.getcwd())
    tap_home()
    print("tap_events()")
    tap_events()
    event_number = 1
    print("startcheck")
    while check_event_available(event_number):
        print(resize_values*10)
        print("try tapping tap_event")

        tap_event(event_number)

        event_name, end_time = get_event_info()

        event_id = get_event_id_by_name(event_name)
        if not event_id:
            event_id = add_event(event_name, end_time)

        tap_play_event()

        tap_match_info()
        event_type_dir = f'{PARENT_DIR}/{event_name}/'
        event_type_cropped_dir = f'{PARENT_DIR}/{event_name}crop/'
        capture_screenshot(PARENT_DIR, event_name, f"{event_name}_1-2")
        time.sleep(2)
        swipe(1000, 800, 1000, 200)
        time.sleep(1)
        capture_screenshot(PARENT_DIR, event_name, f"{event_name}_3-4")
        time.sleep(2)
        crop_and_save_event_type_images(event_type_dir, event_type_cropped_dir)
        time.sleep(2)


        extract_data = get_full_event_type_list(event_type_cropped_dir)
        serie_numbers = []
        serie_id = 0
        for key, value in extract_data.items():
            print(f'{key}: {value}')
            serie_number = key.split('-')[0]
            race_number = key.split('-')[1]
            if serie_number not in serie_numbers:
                serie_numbers.append(serie_number)
                serie_id = add_series(event_id)

            race_type = value['race_type']
            road_type = value['road_type']
            conditions_json = value['conditions']
            add_race(race_type, road_type, conditions_json, race_number, serie_id)
        tap_home()
        print("tap_events()")
        tap_events()
        event_number += 1



