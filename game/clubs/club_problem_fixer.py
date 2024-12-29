import time
from game.clubs.club_state import ClubState
from game.general.general_game_bot import play_match
from game.general.navigator import go_to_club_page, go_to_event_page
from game.clubs.club_checks import check_club_rewards
from game.general.general_actions import unswipe_slots, tap_req_tab, tap_req_1, tap_req_2, tap_exit_after_go_problem, tap_home
from game.general.general_checks import check_missing_slots, get_nr_available_cars, check_repair_slots, check_play_after_go, get_nav_title, check_reset_hand
from game.general.garage_actions import add_from_garage


# TODO only 1 tap when one req
# TODO TOTAL AVAILABLE CARS CHECKING
# TODO NoneType club_state

def fix_problems(club_state: ClubState, stop_event) -> ClubState:
    if stop_event.is_set():
        return club_state
    problem = club_state.problem
    # No problem
    if problem is None:
        return club_state
    
    if problem not in ('GRAY', 'RED'):
        tap_exit_after_go_problem()
    
    club_state.add_error_count()
    if club_state.error_count >= 3 and club_state.played_matches > 0:
        update_club_state(club_state, problem='EVENT_ENDED', status='FAILED')
        return club_state
        
        

    # EVENT-ENDED Reset game state
    if problem == 'EVENT_ENDED':
        club_state = club_state.reset_game_state()
        update_club_state(club_state, problem='EVENT_ENDED', status='FAILED')
        return club_state
    
    
    if problem == 'CARS_SERVICING':
        club_state = fix_cars_servicing(club_state, stop_event)
    
    if problem == 'REQUIREMENTS':
        club_state = fix_reqs(club_state, stop_event)
    
    if problem == 'OTHER':
        update_club_state(club_state, problem='OTHER', status='FAILED')
        

        
    if problem in ('GRAY', 'RED'):
        if problem == 'RED' and club_state.played_matches > 0 and club_state.error_count > 3:
            update_club_state(club_state, problem='RQ_EXCEEDED', status='WAITING')
        club_state = fix_reqs(club_state, stop_event)


    
    if club_state.club_status == 'FAILED':
        club_state.reset_game_state()
        update_club_state(club_state, problem='OTHER', status='FAILED')
        return club_state       
    
    return club_state
    

def fix_reqs(club_state: ClubState, stop_event) -> bool:
    """
    Attempt to fix missing slots in the club's state by unswiping and fixing requirements.

    Args:
        club_state (ClubState): The current state of the club.

    Returns:
        bool: True if the issue is resolved, False otherwise.
    """
    unswipe_slots()
    if stop_event.is_set():
        return False
    if fix_missing_slots(club_state, stop_event):
        update_club_state(club_state, problem='NONE', status='TESTING')
    else:
        if club_state.played_matches > 0:
            update_club_state(club_state, problem='REQUIREMENTS', status='WAITING')
        else:
            if fix_missing_slots(club_state, stop_event):
                update_club_state(club_state, problem='NONE', status='TESTING')
            else:
                update_club_state(club_state, problem='OTHER', status='FAILED')
    return club_state


def fix_cars_servicing(club_state: ClubState, stop_event) -> ClubState:
    """
    Handles cars in servicing by checking repair slots, unswiping if necessary, and fixing missing slots.
    Updates the club's state based on whether the issues are resolved.

    Args:
        club_state (ClubState): The current state of the club.

    Returns:
        ClubState: The updated state of the club.
    """
    repair_slots = check_repair_slots()

    # Unswipe repair slots with a brief pause
    for slot in repair_slots:
        unswipe_slots(slot)
        time.sleep(0.5)
        
    if stop_event.is_set():
        return False
    # Try to fix missing slots; update the club state accordingly
    if fix_missing_slots(club_state, stop_event):
        update_club_state(club_state, problem='NONE', status='TESTING')
    else:
        if club_state.played_matches > 0:
            update_club_state(club_state, problem='CARS_SERVICING', status='WAITING')
        else:
            if fix_reqs(club_state, stop_event):
                update_club_state(club_state, problem='NONE', status='TESTING')
            else:
                update_club_state(club_state, problem='OTHER', status='FAILED')
    return club_state


def update_club_state(club_state: ClubState, problem: str, status: str):
    """
    Helper function to update the problem and status in the club's state.

    Args:
        club_state (ClubState): The current state of the club.
        problem (str): The new problem state.
        status (str): The new status of the club.
    """
    club_state.set_problem(problem)
    club_state.set_club_status(status)
    
    
def fix_missing_slots(club_state: ClubState, stop_event) -> ClubState:
    """
    Attempt to fix missing slots in the club's state by unswiping and fixing requirements.

    Args:
        club_state (ClubState): The current state of the club.

    Returns:
        bool: True if the issue is resolved, False otherwise.
    """
    if stop_event.is_set():
        return False
    missing_slots = check_missing_slots()
    req_list = club_state.req_list

    nav_title = get_nav_title()
    if nav_title == 'OVERVIEW':
        return False
    
    if not handle_req_tab_logic(req_list):
        return False

    if missing_slots:
        if sum(req_list) > 5:
            succes = handle_more_than_five_slots(req_list, missing_slots, stop_event)
        else:
            succes = handle_five_or_fewer_slots(req_list, missing_slots, stop_event)

        if not succes:
            if check_club_rewards():
                return True
            if len(check_missing_slots()) == 0:
                return True
            return False
    return True

def handle_req_tab_logic(req_list):
    """
    Manages the logic for switching between requirement tabs based on the provided list of requirements.
    
    The function toggles the requirement tabs depending on the availability of resources (e.g., cars).
    If multiple requirement tabs are needed, it checks both tabs in sequence, ensuring that the number 
    of available cars meets the requirements in each tab. If any condition fails, the process stops, and 
    the function returns False. Otherwise, the function returns True upon successful completion.

    Args:
        req_list (list): A list where each element represents the number of cars required for a specific tab.
                         - req_list[0]: Number of cars required for the first tab.
                         - req_list[1]: Number of cars required for the second tab.

    Returns:
        bool: 
            - True if the requirement tab logic is handled successfully and sufficient cars are available.
            - False if the number of available cars is insufficient for any requirement.

    Behavior:
        - If `req_list[1]` is not 0, it first switches to the second requirement tab.
        - If the number of available cars is insufficient in either tab, it returns False.
        - If `req_list[1] == 0`, it only checks the first tab.
        - Requirement tabs are toggled according to the car availability checks.
    """
    if req_list[1] != 0:
        switch_to_req_tab(2)
        if req_list[1] > get_nr_available_cars():
            return False
        # TOGGLE 1-OFF|2-ON
        switch_to_req_tab(0)
        if req_list[0] > get_nr_available_cars():
            return False
        #TOGGLE 1-ON|2-OFF
        
    else:
        tap_req_tab()
        if req_list[0] > get_nr_available_cars():
            return False
        # TOGGLE REQ
    return True

def switch_to_req_tab(req_num):
    """Switches to a requirement tab and adds a small delay for the UI.
        req_num: 1 or 2 to toggle or 0 for both
    """
    tap_req_tab()
    time.sleep(0.5)
    
    if req_num == 1 or req_num == 0:
        tap_req_1()
        
    if req_num == 2 or req_num == 0:
        tap_req_2()
        
    time.sleep(0.5)
    tap_req_tab()
    time.sleep(0.5)

def handle_more_than_five_slots(req_list, missing_slots, stop_event):
    """Handles cases where the sum of req_list is greater than 5."""
    if req_list[1] < min(missing_slots):
        add_from_garage(stop_event, len(missing_slots))
    elif req_list[1] > max(missing_slots):
        switch_to_req_tab(2)
        add_from_garage(stop_event, len(missing_slots))
    else:
        split_additions_between_req_tabs(stop_event, req_list[1], missing_slots)

def handle_five_or_fewer_slots(req_list, missing_slots, stop_event):
    """Handles cases where the sum of req_list is less than or equal to 5."""
    if req_list[1] == 0:
        add_from_garage(stop_event, len(missing_slots))
    else:
        under_req1 = [x for x in missing_slots if x <= req_list[0]]
        add_from_garage(stop_event, len(under_req1))

        # TOGGLE 1-OFF|2-ON
        switch_to_req_tab(0)
        add_from_garage(stop_event, len(missing_slots) - len(under_req1))

def split_additions_between_req_tabs(stop_event, req_threshold, missing_slots):
    """Splits the additions between req1 and req2 based on the threshold."""
    under_req2 = [x for x in missing_slots if x <= req_threshold]
    
    switch_to_req_tab(2)
    if not add_from_garage(stop_event, len(under_req2)):
        return False

    switch_to_req_tab(2)
    if not add_from_garage(stop_event, len(missing_slots) - len(under_req2)):
        return False

    return True


def fix_unexpected_screens(stop_event, nav_title, expected_screen):
    """Checks if the screen is expected and fixes it if not.
    possibilities for expected: HOME, CLUB, EVENT"""
    if stop_event.is_set():
        return False
    if nav_title == 'OTHER':
        #CHECK IF PLAY AFTER GO then play match
        
        if check_play_after_go() or check_reset_hand():
            play_match()
            to_home_to_expected_screen(expected_screen)
            return True
        else:
            for _ in range(3):
                tap_home()
                time.sleep(0.5)
            nav_title = get_nav_title()
            if nav_title == 'OTHER':
                return False
    to_home_to_expected_screen(expected_screen)
    return True
        
        

def to_home_to_expected_screen(expected_screen):
    SCREENS = ['HOME', 'CLUB', 'EVENTS']
    if (expected_screen not in SCREENS) or expected_screen == 'HOME':
        tap_home()
    elif expected_screen == 'CLUB':
        go_to_club_page()
    elif expected_screen == 'EVENTS':
        go_to_event_page()
    