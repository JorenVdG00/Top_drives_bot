import os
from datetime import datetime
import subprocess
from config import BOT_SCREENSHOTS_DIR
# import dotenv

WINDOWS_ADB_PATH = "/Users/joren/Desktop/adb/platform-tools-latest-windows/platform-tools/"
DIFF_OS = "./"




def set_cwd():
    # Print the current working directory
    print("Current working directory:", os.getcwd())

    # Change to the user's home directory
    os.chdir(os.path.expanduser("~"))
    print("Changed to home directory:", os.getcwd())

    # Change to a specific directory (e.g., WINDOWS_ADB_PATH)
    os.chdir(WINDOWS_ADB_PATH)
    print("Changed to ADB directory:", os.getcwd())

    return WINDOWS_ADB_PATH, DIFF_OS

# Call the function
set_cwd()

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
    os.system(f"adb shell screencap -p /sdcard/screenshot.png")
    os.system(f"adb pull /sdcard/screenshot.png " + filename)
    os.system(f"adb shell rm /sdcard/screenshot.png")
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