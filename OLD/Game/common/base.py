import os
from dotenv import load_dotenv
from datetime import datetime
from contextlib import contextmanager

from config import ADB_SERIAL_CMD, BOT_SCREENSHOTS_DIR

from OLD.Utils.os_utils import set_cwd
from OLD.Utils.file_utils import create_dir_if_not_exists

load_dotenv()


def tap(x, y):
    set_cwd()
    os.system(f"{ADB_SERIAL_CMD} shell input tap {x} {y}")


def swipe(x1, y1, x2, y2, duration=500):
    set_cwd()
    print(x1, y1, x2, y2)
    os.system(f"{ADB_SERIAL_CMD} shell input swipe {x1} {y1} {x2} {y2} {duration}")


def swipe_and_hold(x1, y1, x2, y2, duration=3000, moves_horizontal=True):
    set_cwd()
    os.system(f"{ADB_SERIAL_CMD} shell input swipe {x1} {y1} {x2} {y2} {duration}")
    if moves_horizontal:
        os.system(f"{ADB_SERIAL_CMD} shell input swipe {x1} {y1} {x1} {y2 + 300} 50")
    else:
        os.system(f"{ADB_SERIAL_CMD} shell input swipe {x1} {y1} {x1 + 300} {y1} 50")


def capture_screenshot(name=None, sub_dir=None, parent_dir=BOT_SCREENSHOTS_DIR, ):
    set_cwd()
    enough_args = False
    if parent_dir is None or sub_dir is None or name is None:
        enough_args = False
    else:
        enough_args = True
        create_dir_if_not_exists(parent_dir, sub_dir)
    if not enough_args:
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        # Construct the screenshot filename
        filename = f"{BOT_SCREENSHOTS_DIR}/screenshot_{timestamp}.png"
    else:
        filename = f"{parent_dir}/{sub_dir}/{name}.png"
    # Take the screenshot
    os.system(f"{ADB_SERIAL_CMD} shell screencap -p /sdcard/screenshot.png")
    os.system(f"{ADB_SERIAL_CMD} pull /sdcard/screenshot.png " + filename)
    os.system(f"{ADB_SERIAL_CMD} shell rm /sdcard/screenshot.png")
    print(f"Screenshot saved to {filename}")
    return filename


@contextmanager
def screenshot_context():
    screenshot = capture_screenshot()
    try:
        yield screenshot
    finally:
        remove_screenshot(screenshot)


def remove_screenshot(filename):
    os.remove(filename)
