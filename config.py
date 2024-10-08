import os
from dotenv import load_dotenv
load_dotenv()

DEBUG = True

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Paths relative to the base directory
BOT_SCREENSHOTS_DIR = os.path.join(BASE_DIR, '!!!BOT_SCREENSHOTS!!!')
COORDS_YML = os.path.join(BASE_DIR, 'src', 'coords.yml')


BASIC_WIDTH = 2210
BASIC_HEIGHT = 1248

resize_values = [1.0, 1.0]  # Default resize values

adb_ip = os.getenv('ADB_IP')
adb_port = os.getenv('ADB_PORT')
adb_serial = os.getenv('ADB_SERIAL')


ADB_SERIAL_CMD = f"{adb_serial} {adb_ip}:{adb_port} "

TRACK_NAMES_PATH = os.path.join(BASE_DIR, 'track_names.csv')

SLEEP_TIME_A = 1
SLEEP_TIME_B = 2



def reload_env():
    load_dotenv(override=True)  # Reload and override existing environment variables

    global adb_ip, adb_port, adb_serial, ADB_SERIAL_CMD

    adb_ip = os.getenv('ADB_IP')
    adb_port = os.getenv('ADB_PORT')
    adb_serial = os.getenv('ADB_SERIAL')

    # Recreate the command with updated variables
    ADB_SERIAL_CMD = f"{adb_serial} {adb_ip}:{adb_port} "