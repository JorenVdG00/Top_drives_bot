import os
import subprocess
from config import BOT_SCREENSHOTS_DIR, ADB_SERIAL_CMD
from dotenv import load_dotenv

load_dotenv()

WINDOWS_ADB_PATH = os.getenv('ADB_PATH')


def set_cwd(adb_path=WINDOWS_ADB_PATH, debug=False):
    # Print the current working directory

    print("Current working directory:", os.getcwd()) if debug else None

    # Change to the user's home directory
    os.chdir(os.path.expanduser("~"))
    print("Changed to home directory:", os.getcwd()) if debug else None

    # Change to a specific directory (e.g., WINDOWS_ADB_PATH)
    os.chdir(adb_path)
    print("Changed to ADB directory:", os.getcwd()) if debug else None

    return adb_path


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
