from utils.image_utils import (
    get_resized_image,
    check_consecutive_pixels,
    color_almost_matches,
    check_color_at_location,
    get_color_at_location,
    take_and_use_screenshot,
    screenshot_context,
    open_image,
    close_image
)
from game import COORDSUTILS, CHECK_MAP
from config import logger
from typing import Optional
from ImageTools.extractors.extractor_base import crop_and_read_image



def check_element(
    check_name: str, screenshot: Optional[str] = None, tolerance: int = 15
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
    coord_name = CHECK_MAP.get(check_name)
    if not coord_name:
        logger.error(f"No box-coordinates found for check: {check_name}")
        return None
    
    coords, target_color = COORDSUTILS.get_color_coords(check_name)
    if not coords:
        return None

    if screenshot:
        resized_img = get_resized_image(screenshot)
    else:
        resized_img = get_resized_image()
    return check_color_at_location(
        resized_img, coords, target_color, tolerance=tolerance
    )

def check_go_button(color: str, screenshot: Optional[str] = None) -> bool:
        """Check for 'Go' button of a given color (blue, gray, red)."""
        return check_element(f"{color.lower()}_go", screenshot, tolerance=30)

def check_after_go_unavailable(screenshot: Optional[str] = None) -> bool:
    """Check if the 'After Go Unavailable' message is present."""
    return check_element("after_go_unavailable", screenshot)

def check_play_after_go(screenshot: Optional[str] = None) -> bool:
    """Check if the 'Play After Go' button is present."""
    return check_element("play_after_go", screenshot, tolerance=60)

def check_reset_hand(screenshot: Optional[str] = None) -> bool:
    """Check if the 'Reset Hand' button is present."""
    return check_element("reset_hand", screenshot)
    
def check_accept_skip(screenshot: Optional[str] = None) -> bool:
    """Check if the 'Accept Skip' button is present."""
    return check_element("accept_skip", screenshot)

def check_refresh(screenshot: Optional[str] = None) -> bool:
    """Check if the 'Refresh' button is present."""
    return check_element("refresh", screenshot)

def check_upgrade_after_match(screenshot: Optional[str] = None) -> bool:
    """Check if the 'Upgrade After Match' button is present."""
    return check_element("upgrade_after_match", screenshot)

def check_sort(order: str, screenshot: Optional[str] = None) -> bool:
    """Check for sorting buttons (ascending or descending)."""
    return check_element(f"sort_{order}", screenshot)

def check_is_fusing(screenshot: Optional[str] = None) -> bool:
    return check_element("is_fusing", screenshot)

def check_is_servicing(screenshot: Optional[str] = None) -> bool:
    return check_element("is_servicing", screenshot)

def check_add_to_hand() -> Optional[bool]:
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
    with screenshot_context() as screenshot:
        add_hand = check_element("add_to_hand", screenshot)
        remove_hand = check_element("remove_from_hand", screenshot)

    if not add_hand:
        logger.error("add_to_hand not found")
        return None  # 'add_to_hand' not found
    if remove_hand:
        logger.error("remove_from_hand found")
        return False  # 'remove_from_hand' found
    return True  # 'add_to_hand' found and 'remove_from_hand' not found

def check_event_ended(screenshot: Optional[str] = None) -> bool:
    """Checks if you can claim an event is present."""
    return check_element("claim_event", screenshot)

# Double Check
def check_double_check(screenshot: Optional[str] = None) -> bool:
    """Double checks if you can claim an event."""
    return check_element("double_check", screenshot)


def get_go_button_color() -> str:
    colors = ["blue", "gray", "red"]
    with screenshot_context() as screenshot:
        for color in colors:
            if check_go_button(color, screenshot):
                logger.debug(f"Go button is {color}")
                return color.upper()
    logger.debug("Go button is not visible")
    # If none of above go button is not visible
    return "NONE"

def get_after_go_problem() -> str:
        with screenshot_context() as problem_screenshot_path:
            extracted_text = crop_and_read_image(
                problem_screenshot_path, "go_button_problem", "text_coords"
            )
            if "ended" in extracted_text.lower():
                return "EVENT_ENDED"
            elif "servicing" in extracted_text.lower():
                return "CARS_SERVICING"
            elif "you need" in extracted_text.lower():
                return "REQUIREMENTS"
            else:
                logger.error(f"Error in problems extracted text: {extracted_text}")
                return "OTHER"

        # Slot Checks

def check_slots(start_key: str, step_key: str, screenshot=None) -> list[int]:
    """
    Checks for slots (e.g., missing or repair) by comparing the color of the slots in a sequence.

    Args:
        start_key (str): The key name for the starting coordinates and color.
        step_key (str): The key name for the step coordinates and color for subsequent slots.
        screenshot: Optional screenshot to check. If not provided, it will capture a new screenshot.

    Returns:
        list[bool]: (1-5)A list of booleans where each entry corresponds to whether a slot matches the target color.
    """

    # Get the starting coordinates and color
    coords, target_color = COORDSUTILS.get_color_coords(start_key)
    step_coords, _ = COORDSUTILS.get_color_coords(
        step_key
    )  # Get the step for the next slot's X coord
    start_x, y = coords
    step_x = step_coords[0]
    # start_x, y = resizer.resize_coordinates(coords[0], coords[1])
    # step_x, _= resizer.resize_coordinates(step_coords[0], coords[1])
    logger.debug(f"start_x: {start_x}, y: {y}, step_x: {step_x}")
    resized_img = get_resized_image(screenshot)
    slots =  [
        color_almost_matches(resized_img.getpixel((start_x + (i * step_x), y)), target_color, 15)
        for i in range(5)
    ]
    for i in range(5):
        x = (start_x + (i * step_x))
        print('x: ', x)
        print(resized_img.getpixel((start_x + (i * step_x), y)))

    
    
    
    slot_numbers = [
        i + 1 for i, is_True in enumerate(slots) if is_True
    ]
    logger.info(f"slots: {slot_numbers}")
    return slot_numbers

def check_missing_slots() -> list[int]:
    """
    Checks for missing slots at the start by comparing the color of the slots in a sequence of 5 slots.

    Args:
        screenshot: Optional screenshot to check. If not provided, it will capture a new screenshot.

    Returns:
        List[bool]: (1-5) A list of booleans where each entry corresponds to whether a slot is missing.
    """
    missing_slots = check_slots("missing_slots_start", "missing_slots_step")
    logger.info(f"missing_slots: {missing_slots}")
    return missing_slots

def check_repair_slots() -> list[int]:
    """
    Checks for repair slots by comparing the color of the slots in a sequence of 5 slots.

    Returns:
        List[bool]: A list of booleans where each entry corresponds to whether a slot needs repair.
    """
    # broken_slots = check_slots("repair_slots_start", "repair_slots_step")
    # broken_slot_numbers = [
    #     i + 1 for i, is_broken in enumerate(broken_slots) if is_broken
    # ]
    # logger.info(f"Broken slots: {broken_slot_numbers}")
    # return broken_slot_numbers
    slot_numbers = check_slots('repair_slots_start', 'repair_slots_step')
    logger.info(f"repair_slots: {slot_numbers}")
    return slot_numbers

def get_nr_available_cars() -> int:
    start_coords, target_color = COORDSUTILS.get_color_coords("empty_garage_slot")
    step_coords, _ = COORDSUTILS.get_color_coords("empty_garage_slot_step")    
    available_cars = 0        
    resized_img = get_resized_image()
    for i in range(5):
        x = start_coords[0] + (i//2 * step_coords[0])
        y = start_coords[1] + (i%2 * step_coords[1])
        color = get_color_at_location(resized_img, (x, y))
        if not color_almost_matches(color, target_color, 25):
            available_cars += 1        
        logger.debug(f"Total Available cars {available_cars}")
    return available_cars
        
        
def get_sort_status() -> Optional[str]:
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
    
    

    resized_img = get_resized_image()
    for sort_type in sort_types:
        coords, target_color = COORDSUTILS.get_color_coords(f"sort_{sort_type}")

        # Handle missing coordinates early
        if not coords:
            logger.error(
                f"Failed to find coordinates for {sort_type} sorting."
            )
            return None

        # Retrieve color at the specified location
        color = get_color_at_location(resized_img, coords)
        sort_dict[sort_type] = color

    # Compare colors and determine sort status
    if sort_dict.get("asc") == target_color:
        return "ASC"
    elif sort_dict.get("desc") == target_color:
        return "DESC"
    else:
        return "NONE"

