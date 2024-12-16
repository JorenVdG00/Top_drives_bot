import time
from config import logger
from game.general.general_actions import (
    tap_skip_match,
    tap_accept_skip,
    tap_upgrade_after_match,
    tap_claim_event,
    tap_play_after_go,
    swipe_cars_to_slots_in_match,
    tap_garage_car,
    tap_hand_slot
)
from game.general.general_checks import (
    check_accept_skip,
    check_upgrade_after_match,
    check_event_ended,
    check_double_check,
    check_play_after_go,
    check_reset_hand,
)
from utils.image_utils import take_and_use_screenshot


# * SKIP MATCH
def skip_match():
    """
    Skip a match by continuously tapping the 'Skip' button until the 'Accept' button appears, then tap it. After that, tap the 'Skip' button 3 more times to ensure that the match is fully skipped. If an 'Upgrade After Match' button appears, tap it to upgrade the match reward as well.

    Returns:
        None
    """
    while not check_accept_skip():
        tap_skip_match()
        time.sleep(3)
    tap_accept_skip()

    for i in range(3):
        tap_hand_slot(1)
        logger.debug(f"tapping after skip...{i}")
        time.sleep(0.5)

    if check_upgrade_after_match():
        tap_upgrade_after_match()
        time.sleep(1)


    for i in range(3):
        tap_hand_slot(1)
        logger.debug(f"tapping after skip...{i}")
        time.sleep(1)

# * CLAIM EVENT
def claim_event():
    can_claim, double_check = True, True
    while can_claim and double_check:
        with take_and_use_screenshot() as screenshot:
            can_claim = check_event_ended(screenshot)
            if can_claim:
                double_check = check_double_check(screenshot)
                if double_check:
                    tap_claim_event()


# ! split event|Clubs
def tap_blue_go_button():
    tap_blue_go_button()
    time.sleep(1)
    if check_play_after_go:
        play_match()
    else:
        return False
        # fix_after_go_problems()





def play_match():
    
    # Tap play button
    """
    Play a match by executing a series of actions in sequence.

    This function performs the following steps:
    1. Taps the play button after 'Go' has been tapped.
    2. Waits for a short duration to ensure the action is registered.
    3. Swipes cars into the available slots until the hand is reset.
    4. Skips the match process.
    
    Returns:
        str 'MATCH PLAYED' if the match is successfully played.
    """
    tap_play_after_go()
    time.sleep(4)

    can_swipe = True
    # Swipe cars to slots
    while can_swipe:
        swipe_cars_to_slots_in_match()
        time.sleep(1)
        can_swipe = check_reset_hand()

    # Skip match
    skip_match()
    
    
       
    #TODO: remove this
    # time.sleep(1)
    # for i in range(3):
    #     tap_garage_car(2, 3)
    #     logger.debug(f"tapping after skip...{(i+3)}")
    #     time.sleep(0.5)
    
    return 'MATCH PLAYED'
    
    
    
    


    
