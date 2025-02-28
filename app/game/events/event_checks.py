from game import COORDSUTILS
from general.general_checks import check_element, logger, get_resized_image


def check_prize_star_1(screenshot=None) -> bool:
    """Checks if the first prize star is present."""
    return check_element('prize_star_1', screenshot)

def check_prize_star_2(screenshot=None) -> bool:
    """Checks if the second prize star is present."""
    return check_element('prize_star_2', screenshot)

def check_prize_star_3(screenshot=None) -> bool:
    """Checks if the third prize star is present."""
    return check_element('prize_star_3', screenshot)

# Prize Card Checks
def check_prize_card_start(screenshot=None) -> list[int]:
    """
    Checks the availability of prize cards by comparing the color of each card on the screen.

    This function retrieves the starting coordinates and target color of the prize cards.
    It then iterates through 15 possible prize card positions, checking if the color matches the target color.

    Args:
        screenshot: Optional screenshot to check. If not provided, it will capture a new screenshot.

    Returns:
        list[int]: A list of remaining prize cards where each entry corresponds to a matching card position.
    """
    prize_cards_left = []

    start_coords, target_color = COORDSUTILS.get_color_coords('prize_card_start')
    step_coords, _ = COORDSUTILS.get_color_coords('prize_card_step')

    if start_coords:
        resized_img = get_resized_image(screenshot)
        
        prize_cards_left = [
            i for i in range(15)
            if resized_img.getpixel((
                start_coords[0] + (i % 5) * step_coords[0],
                start_coords[1] + (i // 5) * step_coords[1]
            )) == target_color
        ]

    else:
        logger.debug(f'No prize card coords found')
    return prize_cards_left 

# Ticket Checks
def check_ticket(screenshot=None) -> bool:
    """Checks if a ticket is available."""
    return check_element('ticket', screenshot)

def check_empty_ticket(screenshot=None) -> bool:
    """Checks if the ticket slot is empty."""
    return check_element('empty_ticket', screenshot)

# Event Requirements Not Met
def check_event_reqs_not_met(screenshot=None) -> bool:
    """Checks if event requirements are not met."""
    return check_element('event_reqs_not', screenshot)

