from config import logger
from app.utils.ImageTools.image_utils import take_and_use_screenshot
from game.general.general_actions import tap_claim_event
from game.general.general_checks import check_event_ended, check_double_check
from game.clubs.club_checks import check_club_rewards
from game.clubs.club_actions import tap_claim_club_reward

def claim_event():
    """
    Continuously checks if an event has ended and can be claimed. When an event can be claimed, it will tap the 'Claim' button.

    Returns:
        None
    """
    can_claim, double_check = True, True
    while can_claim and double_check:
        with take_and_use_screenshot() as screenshot:
            can_claim = check_event_ended(screenshot)
            if can_claim:
                double_check = check_double_check(screenshot)
                if double_check:
                    tap_claim_event()

def claim_club_event():
    """Check if there are club rewards available to claim, and claim them if available.

    Returns:
        bool: True if rewards were claimed, False otherwise
    """
    if check_club_rewards():
        logger.debug("Claiming club rewards...")
        tap_claim_club_reward()
        return True
    return False
