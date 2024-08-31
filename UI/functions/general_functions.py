import os
import math
from datetime import datetime
import subprocess
from config import BOT_SCREENSHOTS_DIR, ADB_SERIAL_CMD
from dotenv import load_dotenv

load_dotenv()

WINDOWS_ADB_PATH = os.getenv('ADB_PATH')




def set_cwd(adb_path=WINDOWS_ADB_PATH):
    # Print the current working directory
    print("Current working directory:", os.getcwd())

    # Change to the user's home directory
    os.chdir(os.path.expanduser("~"))
    print("Changed to home directory:", os.getcwd())

    # Change to a specific directory (e.g., WINDOWS_ADB_PATH)
    os.chdir(adb_path)
    print("Changed to ADB directory:", os.getcwd())

    return adb_path


# # Call the function
# set_cwd()


def tap(x, y):
    os.system(f"{ADB_SERIAL_CMD} shell input tap {x} {y}")


def swipe(x1, y1, x2, y2):
    os.system(f"{ADB_SERIAL_CMD} shell input swipe {x1} {y1} {x2} {y2}")


def capture_screenshot(parent_dir=None, sub_dir=None, name=None):
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


def remove_screenshot(filename):
    os.remove(filename)


def run_subprocess_from_path(command, path=WINDOWS_ADB_PATH):
    try:
        # Start the process in the specified path
        process = subprocess.Popen(command, cwd=path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True)

        # Capture output and errors
        stdout, stderr = process.communicate()

        # Print the output and error (if any)
        if stdout:
            print("Output:\n", stdout)
            return stdout
        if stderr:
            print("Errors:\n", stderr)
    except Exception as e:
        print("An error occurred:", e)
    return None


def color_distance(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1[:3], c2[:3])))  # Ignore the alpha channel


def color_almost_same(color, matching_color, tolerance=10):
    print(color_distance(color, matching_color))
    return color_distance(color, matching_color) < tolerance


def create_dir_if_not_exists(parent_dir, sub_dir):
    # Create the full path for the subdirectory
    full_path = os.path.join(parent_dir, sub_dir)

    # Check if the directory already exists
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        print(f"Directory '{full_path}' created.")
    else:
        print(f"Directory '{full_path}' already exists.")
