import os
import json
import pytesseract
from dotenv import load_dotenv
import logging

load_dotenv()

# Set up Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


DEBUG = True

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Paths relative to the base directory
BASICS_DIR = os.path.join(BASE_DIR, "basics")
UI_DIR = os.path.join(BASE_DIR, "UI")
BOT_SCREENSHOTS_DIR = os.path.join(UI_DIR, "bot_screenshots")
COORDS_YML = os.path.join(BASE_DIR, "coords.yml")
# CONFIG_FILE = os.path.join(BASE_DIR, "config.json")


# def load_config():
#     """Load configuration from the JSON file."""
#     if not os.path.exists(CONFIG_FILE):
#         with open(CONFIG_FILE, "w") as file:
#             json.dump(
#                 {"adb_ip": "127.0.0.1", "adb_port": 5555, "adb_serial": "adb -s"}, file
#             )
            
#     # Load the configuration
#     with open(CONFIG_FILE, "r") as file:
#         return json.load(file)


# def save_config(config):
#     """Save configuration to the JSON file."""
#     with open(CONFIG_FILE, "w") as file:
#         json.dump(config, file, indent=4)


# # Load the configuration
# config = load_config()

# # Access configuration values
# adb_ip = config.get("adb_ip")
# adb_port = config.get("adb_port")
# adb_serial = config.get("adb_serial")

adb_ip = os.getenv("ADB_IP")
adb_port = os.getenv("ADB_PORT")
adb_serial = os.getenv("ADB_SERIAL")

BASIC_WIDTH = 2210
BASIC_HEIGHT = 1248

resize_values = [1.0, 1.0]  # Default resize values


ADB_SERIAL_CMD = f"{adb_serial} {adb_ip}:{adb_port} "

TRACK_NAMES_PATH = os.path.join(BASE_DIR, "track_names.csv")

logger = logging.getLogger(__name__)

# Set log level based on the debug flag
if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

    # Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)

# Create a log format
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)


def reload_env():
    load_dotenv(override=True)  # Reload and override existing environment variables

    global adb_ip, adb_port, adb_serial, ADB_SERIAL_CMD

    adb_ip = os.getenv("ADB_IP")
    adb_port = os.getenv("ADB_PORT")
    adb_serial = os.getenv("ADB_SERIAL")

    # Recreate the command with updated variables
    ADB_SERIAL_CMD = f"{adb_serial} {adb_ip}:{adb_port} "


# def update_adb_config(ip=None, port=None, serial=None):
#     """Update and save the ADB configuration."""
#     global adb_ip, adb_port, adb_serial, ADB_SERIAL_CMD, config

#     if ip:
#         adb_ip = ip
#         config["adb_ip"] = ip
#     if port:
#         adb_port = port
#         config["adb_port"] = port
#     if serial:
#         adb_serial = serial
#         config["adb_serial"] = serial

#     # Update the serialized command
#     ADB_SERIAL_CMD = f"{adb_serial} {adb_ip}:{adb_port}"

#     # Save the updated configuration to file
#     save_config(config)
