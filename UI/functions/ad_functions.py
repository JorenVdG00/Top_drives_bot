from PIL import Image
import os
import random
from datetime import datetime
import time
import subprocess
from .general_functions import capture_screenshot, remove_screenshot, swipe, tap
from .resize_functions import resize_coordinate, resize_coordinates, resize_ranges, resize_same_factor, \
    calculate_screen_size

resize_values = calculate_screen_size()


# TODO: add tap_home to generalgamefunc
def tap_home():
    print("tapping home")
    x1, x2, y1, y2 = resize_ranges(940, 1030, 20, 115, resize_values)
    x, y = random.randint(x1, x2), random.randint(y1, y2)
    tap(x, y)
    time.sleep(2)


def tap_ads():
    print("tapping ads")
    x1, x2, y1, y2 = resize_ranges(300, 420, 1120, 1200, resize_values)
    x, y = random.randint(x1, x2), random.randint(y1, y2)
    tap(x, y)
    time.sleep(2)


def tap_ad(ad_number: int = 1):
    print("tapping ad")
    x1, x2 = resize_same_factor(150, 350, resize_values[0])
    if ad_number == 1:
        y1, y2 = resize_same_factor(280, 360, resize_values[1])
    elif ad_number == 2:
        y1, y2 = resize_same_factor(600, 680, resize_values[1])
    else:
        y1, y2 = resize_same_factor(900, 980, resize_values[1])
    x, y = random.randint(x1, x2), random.randint(y1, y2)
    tap(x, y)
    time.sleep(35)


def tap_exit():
    print("tapping exit")
    x1, x2, y1, y2 = resize_ranges(2175, 2180, 35, 40, resize_values)
    x, y = random.randint(x1, x2), random.randint(y1, y2)
    tap(x, y)
    time.sleep(2)


def check_back_ingame():
    print("checking back in game")
    x, y = resize_coordinates(750, 50, resize_values)
    ingame_color = (213, 213, 213, 255)
    google_play_color = (255, 255, 255, 255)
    img_path = capture_screenshot()
    img = Image.open(img_path)
    remove_screenshot(img_path)
    color = img.getpixel((x, y))
    if color == ingame_color:
        print("back in game")
        return True
    elif color == google_play_color:
        print("entered google play store")
        x, y = resize_coordinates(2134, 1211, resize_values)
        tap(x, y)
        time.sleep(1)
        x, y = resize_coordinates(15, 180, resize_values)
        tap(x, y)
        time.sleep(1)
        return False
    else:
        print("not back in game")
        return False


def is_last_ad(ad_number: int = 1):
    print("checking last ad")
    y = 325 * (ad_number - 1) + 500
    x, y = resize_coordinates(2140, y, resize_values)
    img_path = capture_screenshot()
    img = Image.open(img_path)
    remove_screenshot(img_path)
    color = img.getpixel((x, y))
    if color == (0, 255, 0, 255):
        print("last ad")
        return True
    else:
        print("not last ad")
        return False


def watch_ads():
    tap_home()
    tap_ads()
    ad_number = 1
    print("watching ads")
    while ad_number <= 3:
        tap_ad(ad_number)
        tap_exit()
        if not check_back_ingame():
            tap_exit()
        if is_last_ad(ad_number):
            ad_number += 1
