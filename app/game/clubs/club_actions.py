import time
from config import logger
from game.general.general_actions import tap_action, swipe_and_hold_action  # Import necessary functions
from game.clubs.club_checks import check_club_rewards

# Function to tap on the "clubs" action
def tap_clubs():
    """
    Tap the 'Clubs' button in the events menu.

    Returns:
        None
    """
    
    tap_action("clubs")

# Function to tap on "claim_clubs"
def tap_claim_club_reward():
    """
    Tap the 'Claim' button when a club reward is available.

    Returns:
        None
    """
    tap_action("claim_clubs")

# Function to tap on "play_in_club"
def tap_play_in_club():
    """
    Tap the 'Play' button when in a club-event screen.

    Returns:
        None
    """
    tap_action("play_in_club")

# Function to tap on "play_club"
def tap_play_club():
    """
    Tap the 'Play' button when clicked on a club-event in club-page to go to the club-event screen.

    Returns:
        None
    """

    tap_action("play_club")

# Function to tap on a specific club event
def tap_club_event(number: int):
    """Tap a club event based on the number (starting from 0)."""
    if number > 2:
        number = number % 3
    tap_action(f"club_event_{number + 1}")

# Function to tap "back_club"
def tap_back_club():
    """
    Tap the 'Back' button when clicked on a club-event to go back to the clubs-page.

    Returns:
        None
    """
    tap_action("back_club")


# Function to tap the "exit_info" action
def tap_exit_info():
    """
    Tap the 'Exit Info' button when clicked on the info screen.

    Returns:
        None
    """
    tap_action("exit_info")

    
# Function to swipe up in the clubs section
def swipe_up_clubs(times: int = 1):
    """Swipe up in the clubs section to view 3 new club-events.

    Args:
        times (int, optional): The number of times to swipe up. Defaults to 1.

    Returns:
        None
    """
    for _ in range(times):
        swipe_and_hold_action("swipe_up_clubs")
        time.sleep(0.2)


def claim_club_rewards():
    if check_club_rewards():
        logger.debug("Claiming club rewards...")
        tap_claim_club_reward()
        return True
    return False