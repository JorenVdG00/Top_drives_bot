import time
from config import logger
from game.clubs.club_state import ClubState

from game.general.general_actions import tap_go, tap_back
from game.general.general_checks import get_go_button_color, get_after_go_problem, check_play_after_go, get_nav_title
from game.clubs.club_actions import claim_club_rewards, tap_play_club, tap_play_in_club, tap_back_club
from game.clubs.club_checks import check_go_to_club, check_play_in_club_page
from game.clubs.club_problem_fixer import fix_problems, fix_unexpected_screens
from game.clubs.club_picker import pick_club_event, evaluate_club_event, evaluate_active_club_event, setup_active_event
from game.general.general_game_bot import play_match
from game.general.navigator import go_to_club_page


#TODO: reqlist[1] list index out of range when already in a club, and only 1 requirement

def play_club_events(stop_event):
    # Initialize state
    club_state = ClubState()
     
    go_to_club_page()
    
    #! ADD something when go_to_club_Page fails......
    time.sleep(1)
    if claim_club_rewards():
        club_state.reset_game_state()
        
    if check_go_to_club():
        setup_active_event(club_state)
    
    while not stop_event.is_set():
        if claim_club_rewards():
            club_state.reset_game_state()
        if club_state.active_event is not None:
            play_active_event(club_state, stop_event)
        else:
            find_and_start_new_event(club_state, stop_event)
    
    return club_state



def play_active_event(club_state: ClubState, stop_event):
    while club_state.played_matches < 34:
        nav_title = get_nav_title()
        if nav_title not in ('OVERVIEW', 'EVENTS'):
            logger.error(f"NAV TITLE: {nav_title}, Fixing unexpected screen")
            fix_unexpected_screens(stop_event, nav_title, 'CLUB')
        if stop_event.is_set():
            return club_state
        if claim_club_rewards():
            club_state.reset_game_state()
            return club_state
        
        if check_go_to_club():
            tap_play_club()
        if check_play_in_club_page():
            tap_play_in_club()
            time.sleep(1)
            problem = tap_go_and_play()
            if problem != 'MATCH PLAYED':
                club_state.set_problem(problem)
                club_state = fix_problems(club_state, stop_event)
                if club_state.club_status == 'FAILED':
                    club_state.reset_game_state()
                    return club_state
            else:
                club_state.add_played_match()
        else:
            if nav_title == 'EVENTS':
                tap_back()
                
            if nav_title == 'OVERVIEW':
                if not check_go_to_club():
                    club_state.reset_game_state()
                    return club_state
                    
    club_state.set_club_status = 'Maxed out'
    return club_state

def tap_go_and_play():
    # Tapping logic and handling
    """
    Tap the 'Go' button and play a match if possible.

    If the 'Go' button is blue, tap it and wait for the match to start.
    If the match can be played, play it and return None.
    If the match cannot be played, return the problem.
    Problems include:
    - EVENT_ENDED
    - CARS_SERVICING
    - REQUIREMENTS
    - OTHER
    If the 'Go' button is not blue, return the color of the button.
    Colors include:
    - BLUE
    - GRAY
    - RED
    - NONE (if the 'Go' button is not visible)

    :return: MATCH PLAYED, the problem as a string, or the color of the 'Go' button as a string.
    """
    go_button_color = get_go_button_color()
    if go_button_color == "BLUE":
        tap_go()
        time.sleep(2)
        can_play = check_play_after_go()
        if can_play:
            return play_match()
        else:
            problem = get_after_go_problem()
            if problem == "OTHER":
                time.sleep(1)
                can_play = check_play_after_go()
                if can_play:
                    return play_match()
            else:
                return problem
    else:
        return go_button_color


def find_and_start_new_event(club_state: ClubState, stop_event):
    if stop_event.is_set():
        return club_state
    if check_go_to_club():
        setup_active_event(club_state)
        return club_state
    
    if pick_club_event(club_state, stop_event):
        club_state.add_played_match()
    else:
        club_state.reset_game_state()
    return club_state


def tap_blue_go_button():
    tap_blue_go_button()
    time.sleep(1)
    if check_play_after_go:
        play_match()
    else:
        return False
        # fix_after_go_problems()