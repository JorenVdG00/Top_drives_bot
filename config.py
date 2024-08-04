import os

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Paths relative to the base directory
BASICS_DIR = os.path.join(BASE_DIR, 'basics')
UI_DIR = os.path.join(BASE_DIR, 'UI')
BOT_SCREENSHOTS_DIR = os.path.join(UI_DIR, 'bot_screenshots')

BASIC_WIDTH = 2210
BASIC_HEIGHT = 1248

resize_values = None
