from PIL import Image
from config import resize_values
from OLD.UI.functions.resize_functions import resize_coordinates, resize_ranges
from OLD.UI.functions.general_functions import capture_screenshot, remove_screenshot, tap, color_almost_same, swipe, swipe_and_hold
from OLD.ImageTools import car_coords, car_in_garage_coords
from OLD.Utils.image_utils import color_almost_matches, resize_image, screenshot_context
from OLD.Utils.find_coords_n_colors import get_pixel_color
import time
import random


def check_cannot_play():
    print("checking cannot play")
    cannot_play_coords = (720, 750)
    cannot_play_color = (51, 51, 51, 255)
    selected_hand_fault_color = (255, 255, 255, 255)
    selected_hand_fault_coords = (900, 680)
    go_unavailable_color = (72, 91, 114, 255)
    go_unavailable_coords = (1850, 1020)
    img_path = capture_screenshot()
    with Image.open(img_path) as img:
        x, y = resize_coordinates(cannot_play_coords[0], cannot_play_coords[1], resize_values)
        color1 = img.getpixel((x, y))
        x, y = resize_coordinates(selected_hand_fault_coords[0], selected_hand_fault_coords[1], resize_values)
        color2 = img.getpixel((x, y))
        x, y = resize_coordinates(go_unavailable_coords[0], go_unavailable_coords[1], resize_values)
        color3 = img.getpixel((x, y))

    remove_screenshot(img_path)

    print(color1, color2, color3)
    if color_almost_same(color1, cannot_play_color) \
            or color_almost_same(color2, selected_hand_fault_color) \
            or color_almost_same(color3, go_unavailable_color):
        print("cannot play found!")
        time.sleep(1)
        back_x, back_y = 490, 815
        tap(back_x, back_y)
        return True
    else:
        print('cannot play not found')
        return False


def tap_home():
    print("tapping home")
    x1, x2, y1, y2 = resize_ranges(940, 1030, 20, 115, resize_values)
    x, y = random.randint(x1, x2), random.randint(y1, y2)
    tap(x, y)
    time.sleep(2)


def un_swipe_cars(slot=None):
    slot_x, slot_y = resize_coordinates(830, 820, resize_values)
    std_x1, y1, x2, y2 = car_coords['coords']
    x_step = car_coords['step']
    width = x2 - std_x1
    if slot is None:
        start, end = 1, 6
    else:
        start, end = slot, slot + 1
    for car_number in range(start, end):
        x1 = std_x1 + ((car_number - 1) * (width + x_step))
        x2 = x1 + width
        rand_x, rand_y = (random.randint(*resize_ranges(x1 + 30, x2 - 20, y1 + 10, y2 - 10, resize_values)[i:i + 2]) for
                          i in (0, 2))
        swipe(rand_x, rand_y, slot_x, slot_y)
        time.sleep(1)


def tap_requirements_tab():
    print("clicking requirements tab")
    rand_x, rand_y = (random.randint(*resize_ranges(1140, 1160, 150, 170, resize_values)[i:i + 2]) for i
                      in (0, 2))
    tap(rand_x, rand_y)
    time.sleep(2)
    print("clicked requirements tab")


def tap_requirements_1():
    print("clicking requirements tab")
    rand_x, rand_y = (random.randint(*resize_ranges(1140, 1160, 240, 270, resize_values)[i:i + 2]) for i
                      in (0, 2))
    tap(rand_x, rand_y)
    time.sleep(2)
    print("clicked requirement 1")


def tap_requirements_2():
    print("clicking requirements tab")
    rand_x, rand_y = (random.randint(*resize_ranges(1140, 1160, 390, 430, resize_values)[i:i + 2]) for i
                      in (0, 2))
    tap(rand_x, rand_y)
    time.sleep(2)
    print("clicked requirement 2")


def get_sort_toggle(img_path):
    asc_coords = (1966, 163)
    desc_coords = (1966, 181)

    white = (255, 255, 255, 255)

    asc_color = get_pixel_color(img_path, asc_coords[0], asc_coords[1])
    desc_color = get_pixel_color(img_path, desc_coords[0], desc_coords[1])
    if color_almost_matches(asc_color, desc_color, 10):
        return "SORT"
    elif color_almost_matches(asc_color, white, 10):
        return "ASC"
    elif color_almost_matches(desc_color, white, 10):
        return "DESC"


def tap_sort_asc(curr_sort):
    sort_x, sort_y = resize_coordinates(1966, 163, resize_values)
    change_x, change_y = resize_coordinates(110, 560, resize_values)
    taps = 0
    if curr_sort == "SORT":
        taps = 1
    elif curr_sort == "ASC":
        taps = 0
    elif curr_sort == "DESC":
        taps = 2
    tap(sort_x, sort_y)
    time.sleep(0.5)
    for i in range(taps):
        tap(change_x, change_y)
        time.sleep(0.5)
    tap(sort_x, sort_y)


def swipe_left_cars():
    x1_swipe, x2_swipe, y1, y2 = resize_ranges(1600, 495, 300, 400, resize_values)
    swipe_and_hold(x1_swipe, y1, x2_swipe, y1, 2000)
    time.sleep(0.2)


def swipe_cars(start_slot, end_slot, car_collected=0):
    print('swipe_cars')
    for i in range(car_collected // 4):
        swipe_left_cars()
    y_list = [car_in_garage_coords['y_1'], car_in_garage_coords['y_2']]
    x_list = [car_in_garage_coords['x_1'], car_in_garage_coords['x_2'], car_in_garage_coords['x_3']]
    std_x1, y1, x2, y2 = car_coords['coords']
    x_step = car_coords['step']
    width = x2 - std_x1
    cars_added = 0
    for car_number in range(start_slot, end_slot + 1):
        # Determine the appropriate x and y coordinates from x_list and y_list
        x_index = 2 if car_collected ==4 else 0 if car_collected % 4 < 2 else 1
        y_index = 0 if car_collected % 2 == 0 else 1
        start_x = x_list[x_index]
        start_y = y_list[y_index]
        car_collected += 1
        # Perform the swipe action
        x, y = (start_x[0] + start_x[1]) // 2, (start_y[0] + start_y[1]) // 2
        print(x, y)
        x,y = resize_coordinates(x, y, resize_values)
        print('¨¨¨¨¨¨¨¨¨¨¨¨¨¨')

        # hold_then_drag(x, y, rand_x, rand_y)
        tap(x,y)
        time.sleep(1)
        added = add_to_hand()
        if not added:
            car_number -= 1
            cars_added += 1
        if cars_added < 5:
            return
        time.sleep(1)


def get_missing_slots():
    screenshot = capture_screenshot()
    empty_color = (125, 142, 176, 255)
    y = 1120
    x_start = 230
    x_step = 350
    empty_slots = []
    with Image.open(screenshot) as img:
        resized_img = resize_image(img)
        for i in range(5):
            color = resized_img.getpixel(x_start + (x_step * i), y)
            if color_almost_same(color, empty_color, tolerance=15):
                empty_slots.append((i + 1))
    remove_screenshot(screenshot)
    return empty_slots

def add_to_hand():
    can_add_color = (102, 102, 102, 255)
    tap_x, tap_y = resize_coordinates(250, 780, resize_values)
    exit_x, exit_y = resize_coordinates(100, 750, resize_values)
    with screenshot_context() as screenshot:
        with Image.open(screenshot) as img:
            color = img.getpixel((tap_x, tap_y))
            if color_almost_matches(color, can_add_color, 10):
                tap(tap_x, tap_y)
                return True
            else:
                tap(exit_x, exit_y)
                return False

from OLD.UI.functions.resize_functions import calculate_screen_size

if __name__ == '__main__':
    resize_values = calculate_screen_size()
    # x1,x2, y1,y2 = resize_ranges(800, 450,  400, 1100, resize_values)
    # print(x1,x2,y1,y2)
    # hold_then_drag(x1, y1, x2, y2)
    swipe_cars(start_slot=1, end_slot=5, car_collected=0)