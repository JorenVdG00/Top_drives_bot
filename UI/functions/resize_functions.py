import subprocess
from config import BASIC_WIDTH, BASIC_HEIGHT
from .general_functions import set_cwd, run_subprocess_from_path

# import config

global resize_values


def resize_coordinate(value, resize_factor):
    return int(value * resize_factor)


def resize_same_factor(value1: int, value2: int, resize_factor: float):
    return int(value1 * resize_factor), int(value2 * resize_factor)


def resize_coordinates(x: int, y: int, resize_factor: list):
    return resize_coordinate(x, resize_factor[0]), resize_coordinate(y, resize_factor[1])


def resize_ranges(x1: int, x2: int, y1: int, y2: int, resize_factor: list):
    return (resize_coordinate(x1, resize_factor[0]), resize_coordinate(x2, resize_factor[0]),
            resize_coordinate(y1, resize_factor[1]), resize_coordinate(y2, resize_factor[1]))


def calculate_screen_size():
    global resize_values
    windows, diff_os = set_cwd()
    # size_result = subprocess.run(f"{diff_os}adb shell wm size",cwd=windows, shell=True, capture_output=True, text=True)
    command = f"adb shell wm size"
    size_result = run_subprocess_from_path(command)
    print(size_result)
    size = size_result.strip()
    print("size: " + size)
    print("size_result: " + str(size_result))
    # Parse the size information
    if "Physical size: " in size:
        size = size.split("Physical size: ")[1]
        width, height = map(int, size.split("x"))
        print(f"Width: {width}, Height: {height}")
        resize_value = [width / BASIC_WIDTH, height / BASIC_HEIGHT]
        # config.resize_values = resize_values
        return resize_value
