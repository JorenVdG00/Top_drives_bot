import os

from UI.functions.general_functions import capture_screenshot, tap, swipe, remove_screenshot, create_dir_if_not_exists
from UI.functions.resize_functions import resize_coordinates, calculate_screen_size, set_cwd, resize_ranges
from UI.functions.event_functions import tap_event, tap_events, tap_home, get_event_number_inactive, tap_play_event, swipe_left_one_event
# from image_reader.event.event_cropper_V3 import get_event_name, crop_and_save_event_type_images, crop_event_display_img, crop_all_cars_img
# from image_reader.event.event_reader_V2 import get_full_event_type_list
from image_reader.event.event_time import get_time_left_event, calculate_event_end_time
from database.methods.db_adder import add_event, add_series, add_race
from database.methods.db_delete import remove_event_series
from database.methods.db_events import get_event_id_by_name
from database.db_getters import get_event_id_by_name

from ImageTools.Events.event_reader import get_full_correct_list
from ImageTools.cropper.cars import crop_all_hand_cars
from ImageTools.cropper.classify import get_event_name
from ImageTools.Events.event_cropper import crop_event_display_img, crop_and_save_event_type_images
from config import resize_values, BASE_DIR
import random
import time


DB_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.join(DB_DIR, 'temp')



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

    inactive_number, display_img_paths = get_event_number_inactive(True)

    for event_number in range(1, inactive_number):
        event_display_img = display_img_paths[(event_number-1)]
        if event_number != 1:
            for i in range(event_number-1):
                swipe_left_one_event()
    # while check_event_available(event_number):
        # print(resize_values*10)
        print("try tapping tap_event")

        tap_event(1)
        event_name, end_time = get_event_info()
        event_dir = f'{PARENT_DIR}/{event_name}/'
        event_screens_dir = f'{event_dir}/screens/'
        event_type_cropped_dir = f'{event_dir}/cropped_img/'
        cars_dir = f'{event_dir}/cars/'
        crop_event_display_img(event_display_img, event_dir+'display/', 'display')

        event_id = get_event_id_by_name(event_name)
        if not event_id:
            event_id = add_event(event_name, event_dir, end_time)

        tap_play_event()

        # Get Cars Pictures
        cars_screenshot = capture_screenshot(event_dir, 'cars', 'all_cars')
        crop_all_hand_cars(cars_screenshot, cars_dir)
        remove_screenshot(cars_screenshot)

        tap_match_info()
        capture_screenshot(event_dir, 'screens', f"{event_name}_1-2")
        # time.sleep(2)
        #Swipe up for 3-4 serie of event
        x1, x2, y1, y2 = resize_ranges(1000,1000, 800, 200, resize_values)
        swipe(x1, y1, x2, y2)

        time.sleep(1)
        capture_screenshot(event_dir, 'screens', f"{event_name}_3-4")
        # time.sleep(2)
        crop_and_save_event_type_images(event_screens_dir, event_type_cropped_dir)
        # time.sleep(2)


        extract_data = get_full_correct_list(event_type_cropped_dir)
        serie_numbers = []
        serie_id = 0
        remove_event_series(event_id)
        for key, value in extract_data.items():
            # print(f'{key}: {value}')
            serie_number = key.split('-')[0]
            race_number = key.split('-')[1]
            if serie_number not in serie_numbers:
                serie_numbers.append(serie_number)
                serie_id = add_series(event_id, serie_number)

            race_type = value['race_type']
            road_type = value['road_type']
            conditions_json = value['conditions']
            add_race(race_type, road_type, conditions_json, race_number, serie_id)
        tap_home()
        print("tap_events()")
        tap_events()
        print(f'Finished with event-{event_number}')

        event_number += 1

    for rest in display_img_paths:
        remove_screenshot(rest)
    print('ended!!!!')


