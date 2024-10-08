import os

# from OLD.Game.common.base import capture_screenshot
from contextlib import contextmanager
import logging
from config import DEBUG, adb_ip, adb_port
from src.Utils.ImageTools.resize_class import ResizeClass
from src.Utils.Adb.adb_class import AdbClass, AdbCommandRunner
from src.Utils.file_utils import FileUtils
from src.Utils.ImageTools.image_utils import ImageUtils
from src.Utils.ImageTools.Extractor.extractor_base import ExtractorBase


class BotBase:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Set log level based on the debug flag
        if DEBUG:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

            # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)

        # Create a log format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(console_handler)
        
        

        self.resizer = ResizeClass(self.logger)
        self.adb = AdbClass(adb_ip, adb_port, self.logger, self.resizer)
        self.cmd_runner = self.adb.adb_cmd_runner     
        
        self.screen_manager = ScreenshotManager(self.logger, self.cmd_runner)

        self.image_utils = ImageUtils(self.logger, self.screen_manager)
        self.file_utils = self.adb.file_utils
        self.extractor = ExtractorBase(self)


        # self.actions = CommonActions(self.resize)
        # Use composition to include ResizeClass


class ScreenshotManager:
    def __init__(self, logger: logging.Logger, cmd_runner: AdbCommandRunner):
        super().__init__()
        self.screenshot = None
        self.logger = logger
        self.cmd_runner = cmd_runner

    def capture_screenshot(self):
        """
        Capture a screenshot and store it for future use.
        """
        self.logger.debug("Capturing screenshot...")
        self.screenshot = self.cmd_runner.capture_screenshot()  # Your screenshot logic
        self.logger.debug("Screenshot captured.")
        # self.screenshot = capture_screenshot()/
        return self.screenshot

    def remove_screenshot(self, screenshot=None):
        """
        Remove the previously captured screenshot.
        """
        if screenshot is None:
            if self.screenshot:
                self.logger.debug("Deleting screenshot...")
                os.remove(self.screenshot)
                self.logger.debug(f"Deleted screenshot {self.screenshot}")
                self.screenshot = None
        else:
            self.logger.debug("Deleting screenshot...")
            os.remove(screenshot)
            self.logger.debug(f"Deleted screenshot {screenshot}")

    @contextmanager
    def screenshot_context(self):
        """
        Context manager for capturing and automatically removing a screenshot.
        """
        screenshot = self.cmd_runner.capture_screenshot()
        try:
            yield screenshot
        finally:
            self.remove_screenshot(screenshot)


