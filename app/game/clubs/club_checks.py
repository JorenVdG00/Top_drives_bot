from game.general.general_checks import check_element, logger

def check_club_rewards(screenshot=None) -> bool:
    """Checks if club rewards can be collected."""
    logger.debug("Checking if club rewards can be collected...")
    return check_element("club_rewards", screenshot)


def check_play_in_club_page(screenshot=None) -> bool:
    """Checks if in club page can be playe."""
    return check_element("play_in_club", screenshot, tolerance=35)


def check_go_to_club(screenshot=None) -> bool:
    """Checks if there is a selected club that can be played."""
    return check_element("go_to_club", screenshot)

def check_info_icon(screenshot=None) -> bool:
    """Checks if there is not a selected club now there is a info icon."""
    return check_element("info_icon", screenshot)

def check_exit_info(screenshot=None) -> bool:
    """Checks if accidently pressed on info icon."""
    return check_element("exit_info", screenshot)

def check_last_club(screenshot=None) -> bool:
    """Check if the last club is selected"""
    return check_element("last_club", screenshot)    

def check_left_score_is_half(screenshot=None) -> bool:
    """Checks if the left score is halfway."""
    return check_element("left_score_half", screenshot)

def check_right_score_is_half(screenshot=None) -> bool:
    """Checks if the right score is halfway."""
    return check_element("right_score_half", screenshot)