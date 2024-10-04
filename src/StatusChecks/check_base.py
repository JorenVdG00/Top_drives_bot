from src.TopDrives.base_bot import BotBase
from src.Utils.ImageTools.image_utils import ImageUtils
from typing import Optional, List, Union, Tuple


class CheckBase(BotBase):
    """
    This class performs checks on the screen or a screenshot for various game elements.
    """

    def __init__(self):
        """
        Initializes the CheckBase class, setting up color utilities and the check map.
        """
        super().__init__()
        self.color_utils = self.image_utils.color_utils
        self.check_map = {}
        self._initialize_check_map()

    def _get_resized_image(self, screenshot: Optional[str] = None):
        """
        Helper method to get a resized image from either a provided screenshot or the current screen.

        Args:
            screenshot (Optional[str]): The path to a screenshot file.

        Returns:
            Image: Resized image.
        """
        if screenshot:
            img = self.image_utils.open_image(screenshot)
            resized_img = self.resize.resize_img(img)
            self.image_utils.close_image(img)
        else:
            with self.screen_manager.screenshot_context() as screenshot_img:
                resized_img = self.resize.resize_img(screenshot_img)
        return resized_img

    def check_element(
        self, check_name: str, screenshot: Optional[str] = None, tolerance: int = 15
    ) -> Optional[bool]:
        """
        Generalized function to check for any game element on the current screen or in a screenshot.

        Args:
            check_name (str): The name of the element to check for.
            screenshot (Optional[str]): The path to a screenshot file (if provided).
            tolerance (int): Tolerance level for color checking.

        Returns:
            Optional[bool]: True if the element is found, False if not, and None if the coordinates are invalid.
        """
        coords, target_color = self.get_color_coords(check_name)
        if not coords:
            return None

        if screenshot:
            img = self.image_utils.open_image(screenshot)
            resized_img = self.resize.resize_img(img)
            self.image_utils.close_image(img)
        else:
            with self.screen_manager.screenshot_context() as screenshot_img:
                resized_img = self.resize.resize_img(screenshot_img)

        return self.color_utils.check_color_at_location(
            resized_img, coords, target_color
        )

    # Specific checks for game elements, using the generalized function
    def check_go_button(self, color: str, screenshot: Optional[str] = None) -> bool:
        """Check for 'Go' button of a given color (blue, gray, red)."""
        return self.check_element(f"{color}_go", screenshot)

    def check_after_go_unavailable(self, screenshot: Optional[str] = None) -> bool:
        """Check if the 'After Go Unavailable' message is present."""
        return self.check_element("after_go_unavailable", screenshot)

    def check_play_after_go(self, screenshot: Optional[str] = None) -> bool:
        """Check if the 'Play After Go' button is present."""
        return self.check_element("play_after_go", screenshot)

    def check_accept_skip(self, screenshot: Optional[str] = None) -> bool:
        """Check if the 'Accept Skip' button is present."""
        return self.check_element("accept_skip", screenshot)

    def check_refresh(self, screenshot: Optional[str] = None) -> bool:
        """Check if the 'Refresh' button is present."""
        return self.check_element("refresh", screenshot)

    def check_upgrade_after_match(self, screenshot: Optional[str] = None) -> bool:
        """Check if the 'Upgrade After Match' button is present."""
        return self.check_element("upgrade_after_match", screenshot)

    def check_sort(self, order: str, screenshot: Optional[str] = None) -> bool:
        """Check for sorting buttons (ascending or descending)."""
        return self.check_element(f"sort_{order}", screenshot)

    def check_is_fusing(self, screenshot: Optional[str] = None) -> bool:
        return self.check_element("is_fusing", screenshot)

    def check_is_servicing(self, screenshot: Optional[str] = None) -> bool:
        return self.check_element("is_servicing", screenshot)

    def check_add_to_hand(self) -> Optional[bool]:
        """
        Checks the presence of the 'add_to_hand' and 'remove_from_hand' elements
        in the current screenshot context.

        This method uses the screenshot captured by the screen manager to determine
        the presence of the specified UI elements.

        Returns:
            Optional[bool]:
                - None if 'add_to_hand' is not found.
                - False if 'remove_from_hand' is found.
                - True if 'add_to_hand' is found and 'remove_from_hand' is not found.
        """
        with self.screen_manager.screenshot_context() as screenshot:
            add_hand = self.check_element("add_to_hand", screenshot)
            remove_hand = self.check_element("remove_from_hand", screenshot)

        if not add_hand:
            return None  # 'add_to_hand' not found
        if remove_hand:
            return False  # 'remove_from_hand' found
        return True  # 'add_to_hand' found and 'remove_from_hand' not found

    # Event Checks
    def check_event_ended(self, screenshot: Optional[str] = None) -> bool:
        """Checks if you can claim an event is present."""
        return self.check_element("claim_event", screenshot)

    # Double Check
    def check_double_check(self, screenshot: Optional[str] = None) -> bool:
        """Double checks if you can claim an event."""
        return self.check_element("double_check", screenshot)

    def get_color_coords(
        self, name: str
    ) -> Union[Tuple[Tuple[int, int], Tuple[int, int, int, int]], None]:
        return self.file_utils.get_color_coords(name)

    def get_go_button_color(self) -> str:
        colors = ["blue", "gray", "red"]
        with self.screen_manager.screenshot_context() as screenshot:
            for color in colors:
                if self.check_go_button(color, screenshot):
                    return color.upper()

        # If none of above go button is not visible
        return "NONE"

    def get_after_go_problem(self) -> str:
        with self.screen_manager.screenshot_context() as problem_screenshot:
            problem_img = self.image_utils.open_image(problem_screenshot)
            extracted_text = self.extractor.crop_and_read_image(
                problem_img, "go_button_problem", "text_coords"
            )
            if "ended" in extracted_text.lower():
                return "EVENT_ENDED"
            elif "servicing" in extracted_text.lower():
                return "CARS_SERVICING"
            elif "again" in extracted_text.lower():
                return "REQUIREMENTS"
            else:
                self.logger.error(f"Error in problems extracted text: {extracted_text}")
                return "OTHER"

        # Slot Checks

    def check_slots(self, start_key: str, step_key: str, screenshot=None) -> list[int]:
        """
        Checks for slots (e.g., missing or repair) by comparing the color of the slots in a sequence.

        Args:
            start_key (str): The key name for the starting coordinates and color.
            step_key (str): The key name for the step coordinates and color for subsequent slots.
            screenshot: Optional screenshot to check. If not provided, it will capture a new screenshot.

        Returns:
            list[bool]: A list of booleans where each entry corresponds to whether a slot matches the target color.
        """

        # Get the starting coordinates and color
        coords, target_color = self.get_color_coords(start_key)
        step_coords, _ = self.get_color_coords(
            step_key
        )  # Get the step for the next slot's X coord
        start_x, y = coords
        step_x = step_coords[0]

        resized_img = self._get_resized_image(screenshot)
        slots =  [
            resized_img.getpixel((start_x + i * step_x, y)) == target_color
            for i in range(5)
        ]
        
        slot_numbers = [
            i + 1 for i, is_True in enumerate(slots) if is_True
        ]
        self.logger.info(f"slots: {slot_numbers}")
        return slot_numbers

    def check_missing_slots(self) -> list[int]:
        """
        Checks for missing slots at the start by comparing the color of the slots in a sequence of 5 slots.

        Args:
            screenshot: Optional screenshot to check. If not provided, it will capture a new screenshot.

        Returns:
            List[bool]: A list of booleans where each entry corresponds to whether a slot is missing.
        """
        missing_slots = self.check_slots("missing_slots_start", "missing_slots_step")
        self.logger.info(f"missing_slots: {missing_slots}")
        return missing_slots

    def check_repair_slots(self) -> list[int]:
        """
        Checks for repair slots by comparing the color of the slots in a sequence of 5 slots.

        Returns:
            List[bool]: A list of booleans where each entry corresponds to whether a slot needs repair.
        """
        # broken_slots = self.check_slots("repair_slots_start", "repair_slots_step")
        # broken_slot_numbers = [
        #     i + 1 for i, is_broken in enumerate(broken_slots) if is_broken
        # ]
        # self.logger.info(f"Broken slots: {broken_slot_numbers}")
        # return broken_slot_numbers
        slot_numbers = self.check_slots('repair_slots_start', 'repair_slots_step')
        self.logger.info(f"repair_slots: {slot_numbers}")
        return slot_numbers
    
    

    def get_sort_status(self) -> Optional[str]:
        """
        Determines the current sort status ('ASC', 'DESC', or 'NONE')
        by comparing the colors of the sort indicators.

        Returns:
            'ASC': if ascending sort is active,
            'DESC': if descending sort is active,
            'NONE': if no sort is active,
            None: if sorting information cannot be retrieved.
        """
        sort_dict = {}
        sort_types = ["asc", "desc"]

        with self.screen_manager.screenshot_context() as screenshot_img:
            resized_img = self.resize.resize_img(screenshot_img)
            for sort_type in sort_types:
                coords, target_color = self.get_color_coords(f"sort_{sort_type}")

                # Handle missing coordinates early
                if not coords:
                    self.logger.error(
                        f"Failed to find coordinates for {sort_type} sorting."
                    )
                    return None

                # Retrieve color at the specified location
                color = self.color_utils.get_color_at_location(coords)
                sort_dict[sort_type] = color

        # Compare colors and determine sort status
        if sort_dict.get("asc") == sort_dict.get("desc"):
            return "NONE"
        elif sort_dict.get("asc") == target_color:
            return "ASC"
        else:
            return "DESC"

    def _initialize_check_map(self):
        """
        Initialize and update the check_map with predefined checks.
        This method is intended to be called during the object initialization
        to populate the check_map with common checks.
        """
        club_checks = {
            "blue_go": "blue_go",
            "red_go": "red_go",
            "gray_go": "gray_go",
            "after_go_unavailable": "after_go_unavailable",
            "play_after_go": "play_after_go",
            "accept_skip": "accept_skip",
            "refresh": "refresh",
            "upgrade_after_match": "upgrade_after_match",
            "sort_asc": "sort_asc",
            "sort_desc": "sort_desc",
            "add_to_hand": "add_hand",
            "missing_slots_start": "missing_slots_start",
            "missing_slots_step": "missing_slots_step",
            "claim_event": "claim_event",
            "double_check": "double_check",
            "is_fusing": "is_fusing",
            "is_servicing": "is_servicing",
        }
        self.check_map.update(club_checks)
