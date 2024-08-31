from PIL import Image
from config import resize_values
from .resize_functions import resize_coordinate, resize_coordinates
from .general_functions import capture_screenshot, remove_screenshot, tap, color_almost_same
import time


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
