from game import COORDSUTILS
from game.general.general_actions import tap_cmd, tap_action, swipe_and_hold_action, logger

def tap_prize_card(number: int):
    """
    Tap the prize card at a given number (0-14)

    :param number: The number of the prize card to tap (0-14)
    :return: None
    """
    if 0 <= number < 15:
        coords = COORDSUTILS.get_coords("claim_prizes")
        x1, y1, x_step, y_step = coords
        x = x1 + (x_step * (number % 5))
        y = y1 + (y_step * (number // 5))

        tap_cmd(x, y)
    else:
        logger.error(f"Invalid prize card number: {number}")

def tap_event(number: int):
    """
    Tap an event based on the given number.

    Args:
        number (int): The number of the event to tap.

    Returns:
        bool: True if the tap action was successful, False otherwise.
    """
    if number > 2:
        number = number % 3
    bool = tap_action(f'event_{number+1}')
    return bool

def tap_play_event():
    """
    Tap the 'Play' button in the selected event screen.

    Returns:
        bool: True if the tap action was successful, False otherwise.
    """
    bool = tap_action('play_event')
    return bool


def swipe_left_event() -> bool:
    """
    Swipe left on the events screen to scroll to the next event.

    Returns:
        bool: True if the swipe action was successful, False otherwise.
    """
    return swipe_and_hold_action('swipe_left_event')

