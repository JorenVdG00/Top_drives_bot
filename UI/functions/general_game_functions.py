from PIL import Image
from .resize_functions import resize_coordinate, resize_coordinates
from .general_functions import capture_screenshot, remove_screenshot, tap
import time


def check_cannot_play(resize_values):
    print("checking cannot play")
    cannot_play_color = (51, 51, 51, 255)
    selected_hand_fault_color = (27, 31, 40, 255)
    selected_hand_fault_coords = (490, 815)
    img_path = capture_screenshot()
    img = Image.open(img_path)
    x, y = resize_coordinates(720, 750, resize_values)
    color1 = img.getpixel((x, y))
    x, y = resize_coordinates(selected_hand_fault_coords[0], selected_hand_fault_coords[1], resize_values)
    color2 = img.getpixel((x, y))
    remove_screenshot(img_path)
    print(color1, color2)
    if color1 == cannot_play_color or color2 == selected_hand_fault_color:
        print("cannot play found!")
        time.sleep(1)
        tap(x, y)
        return True
    else:
        print('cannot play not found')
        return False

