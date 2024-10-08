import os
import subprocess
from datetime import datetime
from logging import Logger
from dotenv import load_dotenv
from config import ADB_SERIAL_CMD, BOT_SCREENSHOTS_DIR
from src.Utils.file_utils import FileUtils
# from src.Utils.ImageTools.resize_class import ResizeClass

load_dotenv()

WINDOWS_ADB_PATH = os.getenv('ADB_PATH')


class AdbClass:
    """
    The main class that encapsulates ADB-related functionality.

    Attributes:
        adb_cmd_runner: An instance of AdbCommandRunner that runs ADB commands.
        adb_connector: An instance of AdbConnector that handles ADB connection.
    """

    def __init__(self, ip_address: str, port: str, logger: Logger, resize: 'ResizeClass'):
        self.ip_address = ip_address
        self.port = port
        self.logger = logger
        self.file_utils = FileUtils(self.logger)
        self.adb_cmd_runner = AdbCommandRunner(logger, resize, self.file_utils)
        self.adb_connector = AdbConnector(self.ip_address, self.port, logger, self.adb_cmd_runner)
        self.connection = self.check_connection()

    def set_ip_address(self, ip_address: str):
        self.ip_address = ip_address

    def set_port(self, port: str):
        self.port = port
        
    def reload_adb_connector(self):
        self.adb_connector = AdbConnector(self.ip_address, self.port, self.logger, self.adb_cmd_runner)
        self.connection = self.check_connection()
    
    def check_connection(self) -> bool:
        return self.adb_connector.check_adb_connection()

class AdbCommandRunner:
    """
    Class responsible for running various ADB commands like tap, swipe, and screenshot.

    Attributes:
        logger: The logger instance for logging debug and error information.
    """

    def __init__(self, logger: Logger, resize: 'ResizeClass', file_utils: 'FileUtils'):
        self.logger = logger
        self.resize = resize
        self.file_utils = file_utils
        self.set_cwd()

    def tap(self, x: int, y: int):
        """
        Simulate a tap on the screen at the specified coordinates.

        Args:
            x (int): The x-coordinate for the tap.
            y (int): The y-coordinate for the tap.
        """
        rs_x, rs_y = self.resize.resize_coordinates(x,y)
        os.system(f"{ADB_SERIAL_CMD} shell input tap {x} {y}")
        self.logger.info(f"Tapped at ({x}, {y})")

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 500):
        """
        Perform a swipe gesture from one coordinate to another.

        Args:
            x1 (int): The starting x-coordinate.
            y1 (int): The starting y-coordinate.
            x2 (int): The ending x-coordinate.
            y2 (int): The ending y-coordinate.
            duration (int): The duration of the swipe in milliseconds. Default is 500ms.
        """
        rs_x1, rs_x2, rs_y1, rs_y2 = self.resize.resize_ranges(x1, x2, y1, y2)
        os.system(f"{ADB_SERIAL_CMD} shell input swipe {rs_x1} {rs_y1} {rs_x2} {rs_y2} {duration}")
        self.logger.info(f"Swiped from ({rs_x1}, {rs_y1}) to ({rs_x2}, {rs_y2}) in {duration}ms")

    def swipe_and_hold(self, x1: int, y1: int, x2: int, y2: int, duration: int = 3000, moves_horizontal: bool = True):
        """
        Perform a swipe and hold action on the screen.

        Args:
            x1 (int): The starting x-coordinate.
            y1 (int): The starting y-coordinate.
            x2 (int): The ending x-coordinate.
            y2 (int): The ending y-coordinate.
            duration (int): The duration of the swipe in milliseconds. Default is 3000ms.
            moves_horizontal (bool): Whether to make an additional horizontal move after swipe. Default is True.
        """
        rs_x1, rs_x2, rs_y1, rs_y2 = self.resize.resize_ranges(x1, x2, y1, y2)
        os.system(f"{ADB_SERIAL_CMD} shell input swipe {rs_x1} {rs_y1} {rs_x2} {rs_y2} {duration}")
        if moves_horizontal:
            os.system(f"{ADB_SERIAL_CMD} shell input swipe {rs_x1} {rs_y1} {rs_x1} {rs_y2+300} {duration}")
        else:
            os.system(f"{ADB_SERIAL_CMD} shell input swipe {rs_x1} {rs_y1} {rs_x1+300} {rs_y1} {duration}")
        self.logger.info(f"Swiped and held ({rs_x1}, {rs_y1}) to ({rs_x2}, {rs_y2})")

    def capture_screenshot(self, parent_dir: str = None, sub_dir: str = None, name: str = None) -> str:
        """
        Capture a screenshot and save it to a specified directory. If no directory or name is provided,
        it will use the default BOT_SCREENSHOTS_DIR.

        Args:
            parent_dir (str): Parent directory to save the screenshot.
            sub_dir (str): Subdirectory to save the screenshot.
            name (str): Name for the screenshot file.

        Returns:
            str: The full path of the screenshot file.
        """
        self.set_cwd()

        if parent_dir and sub_dir and name:
            self.file_utils.create_dir_if_not_exists(parent_dir, sub_dir)
            filename = f"{parent_dir}/{sub_dir}/{name}.png"
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            self.file_utils.create_dir_if_not_exists(BOT_SCREENSHOTS_DIR)
            filename = f"{BOT_SCREENSHOTS_DIR}/screenshot_{timestamp}.png"

        # Capture the screenshot
        os.system(f"{ADB_SERIAL_CMD} shell screencap -p /sdcard/screenshot.png")
        os.system(f"{ADB_SERIAL_CMD} pull /sdcard/screenshot.png {filename}")
        os.system(f"{ADB_SERIAL_CMD} shell rm /sdcard/screenshot.png")

        self.logger.info(f"Screenshot saved to {filename}")
        return filename

    def set_cwd(self, adb_path: str = WINDOWS_ADB_PATH) -> str:
        """
        Change the current working directory to the specified ADB path.

        Args:
            adb_path (str): The path to set the current working directory. Defaults to WINDOWS_ADB_PATH.

        Returns:
            str: The new working directory path.
        """
        self.logger.debug(f'Current working directory: {os.getcwd()}')

        os.chdir(os.path.expanduser("~"))
        self.logger.debug(f'Setting cwd to {adb_path}')
        os.chdir(adb_path)
        return adb_path

    def run_subprocess_from_path(self, command: str, path: str = WINDOWS_ADB_PATH) -> str | None:
        """
        Run a subprocess command from the specified path and return the output.

        Args:
            command (str): The command to run.
            path (str): The path to run the command in. Default is WINDOWS_ADB_PATH.

        Returns:
            str | None: The standard output from the command or None if there is an error.
        """
        try:
            process = subprocess.Popen(command, cwd=path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True)
            stdout, stderr = process.communicate()

            if stdout:
                self.logger.debug(stdout)
                return stdout
            if stderr:
                self.logger.error(f'Error occurred performing {command}, No Exception:\n {stderr}')
        except Exception as e:
            self.logger.error(f'Error occurred performing {command}:\n {e}')
        return None


class AdbConnector:
    """
    Class responsible for managing the ADB connection to the device.

    Attributes:
        ip_address: The IP address of the device to connect to.
        port: The port used for the ADB connection.
        logger: The logger instance for logging connection information.
        cmd_runner: The AdbCommandRunner instance to run ADB commands.
    """

    def __init__(self, ip_address: str, port: str, logger: Logger, cmd_runner: AdbCommandRunner) -> None:
        self.ip_address = ip_address
        self.port = port
        self.logger = logger
        self.cmd_runner = cmd_runner

    def adb_connect(self):
        """
        Connect ADB to the specified IP address and port.
        """
        self.cmd_runner.set_cwd()
        adb_cmd = f"adb connect {self.ip_address}:{self.port}"
        output = self.cmd_runner.run_subprocess_from_path(adb_cmd)

        # Check if the connection succeeded based on the output
        if "connected" in output or "already connected" in output:
            self.logger.info(f"Successfully connected to {self.ip_address}:{self.port}")
        else:
            self.logger.error(f"Failed to connect to {self.ip_address}:{self.port}")


    # TODO: WHYYY?????
    def connect_adb_to_game(self):
        """
        Shortcut to connect ADB to the game instance.
        """
        self.adb_connect()

    def adb_devices(self) -> str:
        """
        Get the list of devices connected via ADB.

        Returns:
            str: A list of devices connected to ADB.
        """
        adb_devices_cmd = "adb devices"
        output = self.cmd_runner.run_subprocess_from_path(adb_devices_cmd)
        return output

    def check_adb_connection(self) -> bool:
        """
        Check if the ADB connection is established by verifying if the device is listed.

        Returns:
            bool: True if the device is connected, False otherwise.
        """
        output = self.adb_devices()
        if self.port in output:
            self.logger.info(f"ADB is connected to {self.ip_address}:{self.port}")
            return True
        else:
            self.logger.error("ADB connection failed")
            return False
