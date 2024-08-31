import os
from dotenv import load_dotenv
load_dotenv()

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Paths relative to the base directory
BASICS_DIR = os.path.join(BASE_DIR, 'basics')
UI_DIR = os.path.join(BASE_DIR, 'UI')
BOT_SCREENSHOTS_DIR = os.path.join(UI_DIR, 'bot_screenshots')

BASIC_WIDTH = 2210
BASIC_HEIGHT = 1248

resize_values = [1.0, 1.0]  # Default resize values

adb_ip = os.getenv('ADB_IP')
adb_port = os.getenv('ADB_PORT')
adb_serial = os.getenv('ADB_SERIAL')


ADB_SERIAL_CMD = f"{adb_serial} {adb_ip}:{adb_port} "

TRACK_NAMES_PATH = os.path.join(BASE_DIR, 'track_names.csv')