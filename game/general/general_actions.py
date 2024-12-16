import os
import time
from config import ADB_SERIAL_CMD, logger
from utils.os_utils import set_cwd
from game import COORDSUTILS, ACTION_MAP
from game.general.general_checks import get_sort_status


# * BASIC COMMANDS
def tap_cmd(x, y):
    """Tap on the screen at the given coordinates (x, y)."""
    set_cwd()
    os.system(f"{ADB_SERIAL_CMD} shell input tap {x} {y}")


def swipe_cmd(x1, y1, x2, y2, duration=500):
    """Swipe from (x1,y1) to (x2,y2) with a given duration in milliseconds.

    Args:
        x1 (int): Starting x-coordinate
        y1 (int): Starting y-coordinate
        x2 (int): Ending x-coordinate
        y2 (int): Ending y-coordinate
        duration (int, optional): Swipe duration in milliseconds. Defaults to 500.
    """
    set_cwd()
    os.system(f"{ADB_SERIAL_CMD} shell input swipe {x1} {y1} {x2} {y2} {duration}")


def swipe_and_hold_cmd(x1, y1, x2, y2, duration=3000, moves_horizontal=True):
    """Swipe from (x1,y1) to (x2,y2) with a given duration in milliseconds.

    Args:
        x1 (int): Starting x-coordinate
        y1 (int): Starting y-coordinate
        x2 (int): Ending x-coordinate
        y2 (int): Ending y-coordinate
        duration (int, optional): Swipe duration in milliseconds. Defaults to 3000.
        moves_horizontal (bool, optional): Set to True if the swipe moves horizontally, False if vertically. Defaults to True.
    """
    set_cwd()
    os.system(f"{ADB_SERIAL_CMD} shell input swipe {x1} {y1} {x2} {y2} {duration}")
    if moves_horizontal:
        os.system(f"{ADB_SERIAL_CMD} shell input swipe {x1} {y1} {x1} {y2 + 300} 50")
    else:
        os.system(f"{ADB_SERIAL_CMD} shell input swipe {x1} {y1} {x1 + 300} {y1} 50")


# Tapping action
def tap(name: str) -> bool:
    """Tap on the screen at a random point within the box with the given name.

    Args:
        name (str): The name of the box to tap.

    Returns:
        bool: True if the tap was successful, False otherwise.
    """
    coords = COORDSUTILS.get_rand_box_coords(name)
    if coords:
        x, y = coords
        tap_cmd(x, y)
        logger.info(f"Tapped: {name} at ({x}, {y})")
        return True
    else:
        logger.error(f"No Box Coordinates for '{name}' not found in configuration")
        return False


# Swiping action
def swipe(name: str) -> bool:
    """
    Perform a swipe action on the screen from the coordinates obtained for the given name.

    Args:
        name (str): The name of the swipe entry to retrieve coordinates for.

    Returns:
        bool: True if the swipe was successful, False otherwise.
    """
    coords = COORDSUTILS.get_swipe_coords(name)
    if coords:
        x1, y1, x2, y2 = coords
        swipe_cmd(x1, y1, x2, y2)
        logger.info(f"Swiped: {name} ... ({x1}, {y1})-->({x2}, {y2})")
        return True
    else:
        logger.error(f"Coordinates for '{name}' not found in configuration")
        return False


# Swipe and hold action
def swipe_and_hold(name: str) -> bool:
    """
    Perform a swipe and hold action on the screen from the coordinates obtained for the given name.

    Args:
        name (str): The name of the swipe entry to retrieve coordinates for.

    Returns:
        bool: True if the swipe and hold was successful, False otherwise.
    """
    coords = COORDSUTILS.get_swipe_coords(name)
    if coords:
        x1, y1, x2, y2 = coords
        horizontal = abs(x2 - x1) > abs(y2 - y1)
        swipe_and_hold_cmd(x1, y1, x2, y2, moves_horizontal=horizontal)
        logger.info(f"Swiped: {name} ... ({x1}, {y1})-->({x2}, {y2})")
        return True
    else:
        logger.error(f"Coordinates for '{name}' not found in configuration")
        return False


# Swiping between two elements
def swipe_a_to_b(nameA: str, nameB: str) -> bool:
    """
    Perform a swipe action from the coordinates obtained for nameA to the coordinates obtained for nameB.

    Args:
        nameA (str): The name of the first element to swipe from.
        nameB (str): The name of the second element to swipe to.

    Returns:
        bool: True if the swipe was successful, False otherwise.
    """
    coordsA = COORDSUTILS.get_rand_box_coords(nameA)
    coordsB = COORDSUTILS.get_rand_box_coords(nameB)
    if coordsA and coordsB:
        xA, yA = coordsA
        xB, yB = coordsB
        swipe_cmd(xA, yA, xB, yB)
        logger.info(f"Swiped: {nameA}-->{nameB} ... ({xA}, {yA})-->({xB}, {yB})")
        return True
    else:
        logger.error(f"Coordinates for {nameA} and {nameB} not found in configuration")
        return False


# Tapping action from action map
def tap_action(action_name: str) -> bool:
    """
    Perform a tap action on the screen at a random point within the box with the given action name.

    Args:
        action_name (str): The name of the action to tap.

    Returns:
        bool: True if the tap was successful, False otherwise.
    """

    coord_name = ACTION_MAP.get(action_name)
    if coord_name:
        return tap(coord_name)
    else:
        logger.error(f"No box-coordinates found for action: {action_name}")
        return False


# Swiping action from action map
def swipe_action(action_name: str) -> bool:
    """
    Perform a swipe action on the screen using coordinates obtained from the action map for the given action name.

    Args:
        action_name (str): The name of the action to perform a swipe for.

    Returns:
        bool: True if the swipe was successful, False otherwise.
    """
    coord_name = ACTION_MAP.get(action_name)
    if coord_name:
        return swipe(coord_name)
    else:
        logger.error(f"No Swipecoordinates found for action: {action_name}")
        return False


# Swipe and hold from action map
def swipe_and_hold_action(action_name: str) -> bool:
    """
    Perform a swipe and hold action on the screen using coordinates obtained from the action map for the given action name.

    Args:
        action_name (str): The name of the action to perform a swipe and hold for.

    Returns:
        bool: True if the swipe and hold was successful, False otherwise.
    """
    coord_name = ACTION_MAP.get(action_name)
    if coord_name:
        return swipe_and_hold(coord_name)
    else:
        logger.error(f"No Swipecoordinates found for action: {action_name}")
        return False


# COMMON TAPS


def tap_home() -> bool:
    """
    Tap the home button on the screen.

    Returns:
        bool: True if the tap was successful, False otherwise.
    """

    return tap_action("home")


def tap_back() -> bool:
    """
    Tap the back button on the screen.

    Returns:
        bool: True if the tap was successful, False otherwise.
    """
    return tap_action("back")


def tap_events() -> bool:
    """
    Tap the events button on the screen.

    Returns:
        bool: True if the tap was successful, False otherwise.
    """

    return tap_action("events")


def tap_go() -> bool:
    """
    Tap the 'Go' button when in garage.

    Returns:
        bool: True if the tap was successful, False otherwise.
    """
    return tap_action("go")


def tap_play_after_go():
    """
    Tap the 'Play' button after 'Go' button is tapped in garage.

    Returns:
        bool: True if the tap was successful, False otherwise.
    """
    return tap_action("play_after_go")


def tap_skip_match():
    """
    Tap the 'Skip' button during a match.

    Returns:
        bool: True if the tap was successful, False otherwise.
    """
    return tap_action("skip")


def tap_accept_skip():
    """
    Tap the 'Accept' button that appears after tapping the 'Skip' button during a match.

    Returns:
        bool: True if the tap was successful, False otherwise.
    """
    return tap_action("skip_accept")


def tap_claim_event():
    """
    Tap the 'Claim' button when an event ends.

    It will tap the 'Claim' button 10 times with a 1 second delay in between each tap To collect all rewards.

    Returns:
        None
    """
    tap_action("claim_event")
    time.sleep(2)
    for i in range(10):
        tap_action("claim_event")
        time.sleep(1)
    time.sleep(5)


def tap_upgrade_after_match():
    """
    Tap the Cancel Upgrade button if that appears after an event ends.

    Returns:
        bool: True if the tap was successful, False otherwise.
    """

    return tap_action("upgrade_after_match")


def tap_sort_button():
    """
    Tap the Sort button in garage.

    Returns:
        bool: True if the tap was successful, False otherwise.
    """
    return tap_action("sort")


def tap_sort_rq():
    """
    Tap the Sort RQ button in sort menu.

    Returns:
        bool: True if the tap was successful, False otherwise.
    """
    return tap_action("sort_rq")


def tap_req_tab():
    """
    Tap the requirements tab in the garage.

    Returns:
        bool: True if the tap was successful, False otherwise.
    """
    return tap_action("req_tab")


def tap_req_1():    
    """
    Tap the first requirement in the requrements tabs.

    Returns:
        bool: True if the tap was successful, False otherwise.
    """
    return tap_action("req_1")


def tap_req_2():
    """
    Tap the second requirement in the requrements tabs.

    Returns:
        bool: True if the tap was successful, False otherwise.
    """
    return tap_action("req_2")


def tap_reset_hand():
    """
    Tap the 'Reset Hand' button when swiping cars to race-slots.

    Returns:
        bool: True if the tap was successful, False otherwise.
    """
    return tap_action("reset_hand")

# Function to tap on a car in the garage, given its position
def tap_garage_car(garage_x, garage_y):
    """
    Tap a car in the garage at a specified position (garage_x, garage_y).
    The coordinates (garage_x, garage_y) are 1-based, starting from 1.

    Args:
        garage_x (int): The x position of the car in the garage. Must be between 1 and 3 (inclusive).
        garage_y (int): The y position of the car in the garage. Must be between 1 and 2 (inclusive).

    Returns:
        None
    """
    tap_action(f"garage_{garage_x}_{garage_y}")


def tap_add_to_hand():
    """
    Tap the 'Add to Hand' button when clicked on a car in garage to add it to your race hand.

    Returns:
        bool: True if the tap was successful, False otherwise.
    """
    return tap_action("add_to_hand")


def tap_exit_car():
    """
    Tap the 'Exit Car' button when viewing a car in garage.

    Returns:
        bool: True if the tap was successful, False otherwise.
    """
    return tap_action("exit_car")

def tap_exit_after_go_problem():
    return tap_action("close_problem_go")


def tap_hand_slot(slot_number: int):
    """
    Tap a slot in the hand.

    Args:
        slot_number (int): The number of the slot to tap (1-5).

    Returns:
        bool: True if the tap was successful, False otherwise.
    """
    try:
        if not 1 <= slot_number <= 5:
            raise ValueError(
                f"Invalid slot_number: {slot_number}. Must be between 1 and 5."
            )
        else:
            return tap_action(f"hand_{slot_number}")
            
    except ValueError as e:
        logger.error(f"Error tapping hand slot: {e}")
        return False
# SWIPES


def swipe_left_cars() -> bool:
    """
    Swipe the cars to the left.
    """
    return swipe_and_hold_action("swipe_left_cars")
#TODO add test_swipe_left_cars

def unswipe_slots(slot_number: int = None) -> bool:
    """
    Swipes cars from hand slots back to the garage. Swipes all slots if slot_number is None.
    """
    try:
        if slot_number is not None:
            if not 1 <= slot_number <= 5:
                raise ValueError(
                    f"Invalid slot_number: {slot_number}. Must be between 1 and 5."
                )
            swipe_a_to_b(f"hand_{slot_number}", "garage_1_2")
        else:
            for i in range(1, 6):
                logger.debug(f"swiping slot {i} back to garage")
                swipe_a_to_b(f"hand_{i}", "garage_1_2")
                time.sleep(0.5)
        return True
    except Exception as e:
        logger.error(f"Error swiping slots: {e}")
        return False


def swipe_cars_to_slots_in_match(assignments: list[int] = None) -> bool:
    """
    Swipe cars into the slots, optionally based on a list of assignments.
    """
    logger.debug("swiping cars to slots")
    if assignments is None:
        assignments = list(range(1, 6))  # Default swipe 1-5 cars

    for slot_nr, car in enumerate(assignments, start=1):
        logger.debug(f"swiping car {car} to slot {slot_nr}")
        swipe_a_to_b(f"ingame_car{car}", f"ingame_slot{slot_nr}")
    return True


def set_sort(sort: str) -> None:
    if sort.upper() not in ["ASC", "DESC", "NONE"]:
        sort = "ASC"
        
    current_sort_status = get_sort_status()
    logger.debug(f'Status: {current_sort_status}')
    taps = calculate_taps(current_sort_status, sort)
    
    if taps > 0:
        tap_sort_button()
        time.sleep(0.5)
        for _ in range(taps):
            tap_sort_rq()
            time.sleep(0.5)
        time.sleep(0.5)
        tap_go()
    
def calculate_taps(current_sort_status: str, sort_status: str) -> int:
    """
    Calculate the number of taps required to reach the desired sort order.

    Args:
        current_sort_status (str): The current sort status ('ASC', 'DESC', 'NONE').
        sort_order (str): The desired sort order ('ASC', 'DESC').

    Returns:
        int: The number of taps required to set the desired sorting order.
    """
    # Define a dictionary with (current status, desired status) as keys and tap counts as values
    tap_counts = {
        ('ASC', 'ASC'): 0,
        ('ASC', 'DESC'): 1,
        ('DESC', 'ASC'): 2,
        ('DESC', 'DESC'): 0,
        ('NONE', 'ASC'): 1,
        ('NONE', 'DESC'): 0
    }

    # Get the number of taps from the dictionary, defaulting to 0 if the key is not found
    return tap_counts.get((current_sort_status, sort_status.upper()), 0)  
