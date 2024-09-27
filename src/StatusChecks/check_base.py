from src.TopDrives.base_bot import BotBase
from src.Utils.ImageTools.image_utils import ImageUtils
from typing import Tuple, Union


class CheckBase(BotBase):
    """
    This class is responsible for performing various checks on the screen or a provided screenshot
    for different game elements such as buttons, prize stars, tickets, etc.
    """

    def __init__(self):
        """
        Initializes the CheckBase class. Inherits from BotBase and initializes an ImageUtils instance
        for image-related operations.
        """
        super().__init__()
        self.color_utils = self.image_utils.color_utils
        self.check_map = {}
        self._initialize_check_map()

    def check_screen_for(self, check_name: str, tolerance: int = 15) -> bool | None:
        """
        Checks the current screen for a specific game element based on its name.

        Args:
            check_name (str): The name of the element to check for.
            tolerance (int): the tolerance for the distance between color and target color.

        Returns:
            bool | None: Returns True if the color at the specified coordinates matches the target color,
                         False if it doesn't, and None if the coordinates are not found.
        """
        coords, target_color = self.get_color_coords(check_name)
        if coords:
            with self.screen_manager.screenshot_context() as screenshot:
                resized_img = self.resize.resize_img(screenshot)
                if self.color_utils.check_color_at_location(resized_img, coords, target_color):
                    return True
                else:
                    return False
        else:
            return None

    def check_screenshot_for(self, image_path: str, check_name: str, tolerance: int = 15) -> bool | None:
        """
        Checks a provided screenshot for a specific game element based on its name.

        Args:
            image_path (str): The path to the screenshot file.
            check_name (str): The name of the element to check for.
            tolerance (int): the tolerance for the distance between color and target color.

        Returns:
            bool | None: Returns True if the color at the specified coordinates matches the target color,
                         False if it doesn't, and None if the coordinates are not found.
        """
        coords, target_color = self.get_color_coords(check_name)
        if coords:
            img = self.image_utils.open_image(image_path)
            resized_img = self.resize.resize_img(img)
            self.image_utils.close_image(img)

            if self.color_utils.check_color_at_location(resized_img, coords, target_color):
                return True
            else:
                return False
        else:
            return None

    # GO Button Checks
    def check_blue_go_button(self, screenshot=None) -> bool:
        """
        Checks for the presence of the blue 'Go' button on the screen or in a provided screenshot.

        Args:
            screenshot: An optional screenshot to check. If not provided, the current screen is used.

        Returns:
            bool: True if the blue 'Go' button is present, False otherwise.
        """
        if screenshot:
            return self.check_screenshot_for(screenshot, 'blue_go')
        else:
            return self.check_screen_for('blue_go')

    def check_gray_go_button(self, screenshot=None) -> bool:
        """
        Checks for the presence of the gray 'Go' button on the screen or in a provided screenshot.

        Args:
            screenshot: An optional screenshot to check. If not provided, the current screen is used.

        Returns:
            bool: True if the gray 'Go' button is present, False otherwise.
        """
        if screenshot:
            return self.check_screenshot_for(screenshot, 'gray_go')
        else:
            return self.check_screen_for('gray_go')

    def check_red_go_button(self, screenshot=None) -> bool:
        """
        Checks for the presence of the red 'Go' button on the screen or in a provided screenshot.

        Args:
            screenshot: An optional screenshot to check. If not provided, the current screen is used.

        Returns:
            bool: True if the red 'Go' button is present, False otherwise.
        """
        if screenshot:
            return self.check_screenshot_for(screenshot, 'red_go')
        else:
            return self.check_screen_for('red_go')

    # Other Checks
    def check_after_go_unavailable(self, screenshot=None) -> bool:
        """Checks if the 'After Go Unavailable' message is present."""

        if screenshot:
            return self.check_screenshot_for(screenshot, 'after_go_unavailable')
        else:
            return self.check_screen_for('after_go_unavailable')

    def check_play_after_go(self, screenshot=None) -> bool:
        """Checks if the 'Play After Go' button is present."""

        if screenshot:
            return self.check_screenshot_for(screenshot, 'play_after_go')
        else:
            return self.check_screen_for('play_after_go')

    def check_accept_skip(self, screenshot=None) -> bool:
        """Checks if the 'Accept Skip' button is present."""

        if screenshot:
            return self.check_screenshot_for(screenshot, 'accept_skip')
        else:
            return self.check_screen_for('accept_skip')

    def check_refresh(self, screenshot=None) -> bool:
        """Checks if the 'Refresh' button is present."""

        if screenshot:
            return self.check_screenshot_for(screenshot, 'refresh')
        else:
            return self.check_screen_for('refresh')

    def check_upgrade_after_match(self, screenshot=None) -> bool:
        """Checks if the 'Upgrade After Match' button is present."""

        if screenshot:
            return self.check_screenshot_for(screenshot, 'upgrade_after_match')
        else:
            return self.check_screen_for('upgrade_after_match')

    # Sorting Checks
    def check_sort_asc(self, screenshot=None) -> bool:
        if screenshot:
            return self.check_screenshot_for(screenshot, 'sort_asc')
        else:
            return self.check_screen_for('sort_asc')

    def check_sort_desc(self, screenshot=None) -> bool:
        if screenshot:
            return self.check_screenshot_for(screenshot, 'sort_desc')
        else:
            return self.check_screen_for('sort_desc')

    # Hand Checks
    def check_add_to_hand(self, screenshot=None) -> bool:
        if screenshot:
            return self.check_screenshot_for(screenshot, 'add_to_hand')
        else:
            return self.check_screen_for('add_to_hand')

    def check_remove_from_hand(self, screenshot=None) -> bool:
        if screenshot:
            return self.check_screenshot_for(screenshot, 'remove_from_hand')
        else:
            return self.check_screen_for('remove_from_hand')
    # Slot Checks
    def check_missing_slots_start(self, screenshot=None) -> list[bool]:
        """
        Checks for missing slots at the start by comparing the color of the slots
        in a sequence of 5 slots.

        Args:
            screenshot: Optional screenshot to check. If not provided, it will capture a new screenshot.

        Returns:
            list[bool]: A list of booleans where each entry corresponds to whether a slot is missing.
        """
        is_missing_list = []

        # Get the starting coordinates and color
        coords, target_color = self.get_color_coords('missing_slots_start')
        step_coords, _ = self.get_color_coords('missing_slots_step')  # Get the step for the next slot's X coord
        start_x, y = coords
        step_x = step_coords[0]

        # Handle screenshot: use provided or capture a new one
        if screenshot is None:
            with self.screen_manager.screenshot_context() as screenshot:
                resized_img = self.resize.resize_img(screenshot)
        else:
            img = self.image_utils.open_image(screenshot)
            resized_img = self.resize.resize_img(img)
            self.image_utils.close_image(img)

        # Check for missing slots
        for i in range(5):
            x = start_x + (i * step_x)  # Calculate the X coordinate for each slot
            color = resized_img.getpixel((x, y))
            is_missing_list.append(color == target_color)

        return is_missing_list

    # Event Checks
    def check_event_ended(self, screenshot=None) -> bool:
        """Checks if you can claim an event is present."""
        if screenshot:
            return self.check_screenshot_for(screenshot, 'claim_event')
        else:
            return self.check_screen_for('claim_event')

    # Double Check
    def check_double_check(self, screenshot=None) -> bool:
        """Double checks if you can claim an event."""
        if screenshot:
            return self.check_screenshot_for(screenshot, 'double_check')
        else:
            return self.check_screen_for('double_check')

    def get_color_coords(self, name: str) -> Union[Tuple[Tuple[int, int], Tuple[int, int, int, int]], None]:
        return self.file_utils.get_color_coords(name)

    def get_go_button_color(self) -> str:
        with self.screen_manager.screenshot_context as screenshot:
            is_blue = self.check_blue_go_button(screenshot)
            is_gray = self.check_gray_go_button(screenshot)
            is_red = self.check_red_go_button(screenshot)
        if is_blue:
            return 'BLUE'
        if is_gray:
            return 'GRAY'
        if is_red:
            return 'RED'
        # If none of above go button is not visible
        return 'NONE'

    def get_after_go_problem(self) -> str:
        with self.screen_manager.screenshot_context as problem_screenshot:
            problem_img = self.image_utils.open_image(problem_screenshot)
            extracted_text = self.extractor.crop_and_read_image(problem_img, 'go_button_problem', 'text_coords')
            if 'ended' in extracted_text.lower():
                return 'EVENT_ENDED'
            elif 'servicing' in extracted_text.lower():
                return 'CARS_REPAIR'
            else:
                self.logger.error(f'Error in problems extracted text: {extracted_text}')
                return 'OTHER'

    def _initialize_check_map(self):
        """
        Initialize and update the check_map with predefined checks.
        This method is intended to be called during the object initialization
        to populate the check_map with common checks.
        """
        club_checks = {
            'blue_go': 'blue_go',
            'red_go': 'red_go',
            'gray_go': 'gray_go',
            'after_go_unavailable': 'after_go_unavailable',
            'play_after_go': 'play_after_go',
            'accept_skip': 'accept_skip',
            'refresh': 'refresh',
            'upgrade_after_match': 'upgrade_after_match',
            'sort_asc': 'sort_asc',
            'sort_desc': 'sort_desc',
            'add_to_hand': 'add_hand',
            'missing_slots_start': 'missing_slots_start',
            'missing_slots_step': 'missing_slots_step',
            'claim_event': 'claim_event',
            'double_check': 'double_check',
        }
        self.check_map.update(club_checks)
