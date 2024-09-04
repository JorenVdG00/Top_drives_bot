from PIL import Image
import pytesseract
import re
import os
from datetime import timedelta, datetime
from ImageTools import pytesseract
from ImageTools.cropper.coords import time_left_coords
from ImageTools.utils.image_utils import resize_image
from dotenv import load_dotenv

load_dotenv()


def get_time_left_event(image_path):
    with Image.open(image_path) as image:
        resized_image = resize_image(image)
        cropped_image = resized_image.crop(time_left_coords)
        extract_time = pytesseract.image_to_string(cropped_image)
        print("extract: " + extract_time)
        return extract_time


def parse_time_string(time_str):
    """
    Parses a string of format '©) 1d 20h 31m 42s' or '©) 19h 35m 22s' into a timedelta.

    Args:
        time_str (str): The time string to parse.

    Returns:
        timedelta: A timedelta object representing the duration.
    """
    # Regex to extract days, hours, minutes, and seconds
    pattern = r'(\d+d)?\s*(\d+h)?\s*(\d+m)?\s*(\d+s)?'
    matches = re.findall(pattern, time_str.strip())
    print(matches)
    i = 0
    for match in matches:
        if match[3]:
            break
        else:
            i += 1
            if i == len(matches) - 1:
                i = 0
    if matches:
        # Since matches is a list of tuples, we'll take the first match (only one expected)
        match = matches[i]
        days = int(match[0][:-1]) if match[0] else 0
        hours = int(match[1][:-1]) if match[1] else 0
        minutes = int(match[2][:-1]) if match[2] else 0
        seconds = int(match[3][:-1]) if match[3] else 0

        # Return a timedelta object
        return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    else:
        raise ValueError(f"Invalid time string format: {time_str}")


def calculate_event_end_time(duration, current_time=None):
    """
    Calculates the event end time based on the given duration and current time.

    Args:
        duration (timedelta): Duration until the event ends.
        current_time (datetime): The current time. Defaults to now.

    Returns:
        datetime: The calculated event end time.
    """
    time_left = parse_time_string(duration)
    if current_time is None:
        current_time = datetime.now()

    return current_time + time_left
