from PIL import Image
from .general_functions import tap, swipe, swipe_and_hold
from config import BOT_SCREENSHOTS_DIR, resize_values
from .resize_functions import resize_coordinate, resize_coordinates, resize_ranges, resize_same_factor, \
    calculate_screen_size
from ImageTools.utils.image_utils import color_almost_matches, resize_image
import os
import threading
import time
import random


def tap_clubs():
    x1, x2, y1, y2 = resize_ranges(260, 520, 500, 750, resize_values)
    x, y = random.randint(x1, x2), random.randint(y1, y2)
    tap(x, y)
    time.sleep(1)


def claim_club_reward():
    x1, x2, y1, y2 = resize_ranges(1000, 770, 1050, 780, resize_values)
    x, y = random.randint(x1, x2), random.randint(y1, y2)
    tap(x, y)
    time.sleep(1)


def check_club_rewards(img_path):
    x, y = resize_coordinates(1030, 770, resize_values)
    club_reward_color = (25, 200, 212, 255)
    with Image.open(img_path) as img:
        color = img.getpixel((x, y))
        if color_almost_matches(color, club_reward_color):
            return True
        else:
            return False


def has_joined_event(img_path):
    x, y = resize_coordinates(1700, 1160, resize_values)
    play_event_color = (255,196,79,255)

    with Image.open(img_path) as img:
        color = img.getpixel((x, y))
        if color_almost_matches(color, play_event_color):
            return True
        else:
            return False

def swipe_clubs_3_up():
    x1, x2, y1, y2 = resize_ranges(1600, 1600, 1160, 670, resize_values)
    swipe_and_hold(x1, y1, x2, y2, 3000, False)
    time.sleep(0.2)
