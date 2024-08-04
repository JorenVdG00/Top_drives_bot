import os
from datetime import datetime

from config import BOT_SCREENSHOTS_DIR


def tap(x, y):
    os.system(f"adb shell input tap {x} {y}")


def swipe(x1, y1, x2, y2):
    os.system(f"adb shell input swipe {x1} {y1} {x2} {y2}")


def capture_screenshot():
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # Construct the screenshot filename
    filename = f"{BOT_SCREENSHOTS_DIR}/screenshot_{timestamp}.png"
    # Take the screenshot
    os.system("adb shell screencap -p /sdcard/screenshot.png")
    os.system("adb pull /sdcard/screenshot.png " + filename)
    os.system("adb shell rm /sdcard/screenshot.png")
    print(f"Screenshot saved to {filename}")
    return filename


def remove_screenshot(filename):
    os.remove(filename)
