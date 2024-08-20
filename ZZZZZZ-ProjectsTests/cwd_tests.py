import os
from config import BASE_DIR, BOT_SCREENSHOTS_DIR

cwd = os.getcwd()
print(cwd)
this_dir = os.path.dirname(os.path.abspath(__file__))
print(this_dir)
screenshots_dir = os.path.join(this_dir, "screenshots")

screen_dir = "/home/jorenvdg/PycharmProjects/Top_drives_bot/UI/bot_screenshots"
this_dir = "/home/jorenvdg/PycharmProjects/Top_drives_bot/basics"

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(BASE_DIR)
print(BOT_SCREENSHOTS_DIR)