# from logging import Logger
from typing import Any

from PIL import Image
from config import BASIC_WIDTH, BASIC_HEIGHT, ADB_SERIAL_CMD
from src.Utils.terminal_helper import set_cwd, run_subprocess_from_path
from src.Utils.Adb.adb_connector import connect_adb_to_game
from dotenv import load_dotenv

load_dotenv()
STANDARD_SIZE = (BASIC_WIDTH, BASIC_HEIGHT)


class ResizeClass:
    def __init__(self, logger: 'Logger'):
        self.logger = logger
        self.resize_values = self.calculate_screen_size()

    def resize_coordinate(self, value: int, resize_factor: float) -> int:
        """
        Resize a coordinate value based on the resize factor.

        :param value: The coordinate value to resize.
        :param resize_factor: The factor by which to resize.
        :return: The resized coordinate value.
        """
        return int(value * resize_factor)

    def resize_same_factor(self, value1: int, value2: int, resize_factor: float) -> tuple:
        """
        Resize two coordinate values with the same factor.

        :param value1: The first coordinate value.
        :param value2: The second coordinate value.
        :param resize_factor: The factor by which to resize.
        :return: A tuple containing the resized coordinate values.
        """
        return int(value1 * resize_factor), int(value2 * resize_factor)

    def resize_coordinates(self, x: int, y: int) -> tuple:
        """
        Resize x and y coordinates based on the resize factors.

        :param x: The x coordinate.
        :param y: The y coordinate.
        :return: A tuple containing the resized x and y coordinates.
        """
        return self.resize_coordinate(x, self.resize_values[0]), self.resize_coordinate(y, self.resize_values[1])

    def resize_ranges(self, x1: int, x2: int, y1: int, y2: int) -> tuple[int, int, int, int]:
        """
        Resize a range of coordinates based on the resize factors.

        :param x1: The starting x coordinate.
        :param x2: The ending x coordinate.
        :param y1: The starting y coordinate.
        :param y2: The ending y coordinate.
        :return: A tuple containing the resized coordinates.
        """
        return (
            self.resize_coordinate(x1, self.resize_values[0]), self.resize_coordinate(x2, self.resize_values[0]),
            self.resize_coordinate(y1, self.resize_values[1]), self.resize_coordinate(y2, self.resize_values[1]))

    def calculate_screen_size(self) -> list[Any]:
        """
         Calculate and update the screen size and resize values.

         :return: A list containing the resize factors for width and height.
         """
        # global resize_values
        set_cwd()
        command = f"{ADB_SERIAL_CMD} shell wm size"
        size_result = run_subprocess_from_path(command)
        self.logger.info(f"Size of screen: {size_result}")
        if size_result == None:
            return STANDARD_SIZE
            # TODO: Add error handling
            connect_adb_to_game()
            return self.calculate_screen_size()
        size = size_result.strip()
        self.logger.debug(f"size: {size}")
        # Parse the size information
        if "Physical size: " in size:
            size = size.split("Physical size: ")[1]
            width, height = map(int, size.split("x"))
            self.logger.debug(f"width: {width}, height: {height}")
            resize_value = [width / BASIC_WIDTH, height / BASIC_HEIGHT]
            # resize_values[:] = resize_value
            self.resize_values = resize_value
            self.logger.debug(f"resize_value: {resize_value}")
            # self.logger.debug(f"resize_values: {resize_values}")
            return resize_value

    def resize_img(self, image: Image) -> Image:
        return image.resize(STANDARD_SIZE, Image.Resampling.LANCZOS)
