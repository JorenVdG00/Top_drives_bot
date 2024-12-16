# import time
# from config import logger
# from ImageTools.extractors.extractor_base import

# class EventPicker:
#     def __init__(self):
#         self.best_event = {"name": None, "score": 20000, "number": 0}
#         self.current_number = 0
#         self.game_state = None

#     def set_state_searching(self):
#         self.game_state = "searching"

#     def set_state_trying(self):
#         self.game_state = "trying"

#     def set_state_found(self):

#         self.game_state = "found"

#     def set_state_stop(self):
#         self.game_state = "stop"

#     def get_state(self):
#         return self.game_state

#     def set_best_event(self, best_event):
#         self.best_event = best_event

#     def compare_best_event(self, best_event):
#         if self.best_event["score"] < best_event["score"]:
#             self.best_event = best_event

#     def find_worthy_event(self):
#         number = 0
#         while self.game.active_event == None:
#             if self.game.stop_event.is_set():
#                 return False
#             with self.game.screen_manager.screenshot_context() as screenshot:
#                 if not self.game.checks.check_info_icon(screenshot) and self.game.checks.check_exit_info(screenshot):
#                     self.game.actions.tap_exit_info()
#                 elif self.game.checks.check_last_club(screenshot):
#                     number = 0

#             if number > 2:
#                 self.game.actions.swipe_up_clubs(number // 3)
#                 self.logger.debug(f"swiped up {number // 3} times")

#             self.logger.debug(f"Tapping event {number}")
#             while not self.game.checks.check_go_to_club():
#                 self.game.actions.tap_club_event((number % 3))
#                 time.sleep(0.5)
#                 self.game.claim_club_rewards()
#             event = self.evaluate_club_event()
#             if event != False:
#                 self.game.set_active_event(event)
#                 time.sleep(0.5)
#                 has_active = self.try_club()
#                 if has_active:
#                     # self.set_active_event(event)
#                     return True
#                 else:
#                     self.game.remove_active_event()
#             # NOT WORTHY EVENT
#             number += 1
#             self.game.actions.tap_back_club()


#     def evaluate_club_event(self):
#         pick_score, extracted_data = self.extractor.evaluate_club_pick()
#         req_list = self.extractor.get_req_list(extracted_data)

#         event = {
#             "name": extracted_data["name"],
#             "score": pick_score,
#             "number": self.current_number,
#             "req_list": req_list,
#         }

#         if pick_score < 15:
#             return event
#         elif pick_score is None:
#             return False
#         else:
#             self.compare_best_event(event)
#             return False

#     def try_club(self) -> bool:
#         self.game.actions.tap_play_club()
#         time.sleep(2)

#         # Checking play-button is clickable in club-event
#         if self.game.checks.check_play_in_club_page():
#             self.game.actions.tap_play_in_club()
#             time.sleep(2)
#             self.game.set_sort("ASC")
#             time.sleep(2)
#             if self.game.tap_go_and_play():
#                 return True
#             else:
#                 return False

#         else:
#             self.game.go_to_club_page()
#             return False

from game.clubs.club_checks import (
    check_go_to_club,
    check_exit_info,
    check_info_icon,
    check_last_club,
    check_play_in_club_page
)
from game.clubs.club_actions import (
    claim_club_rewards,
    tap_club_event,
    tap_exit_info,
    swipe_up_clubs,
    tap_play_club,
    tap_play_in_club
)
from game.clubs.club_problem_fixer import fix_problems

from game.general.general_actions import set_sort, tap_go
from game.general.general_checks import get_go_button_color, check_play_after_go, get_after_go_problem
from game.general.general_game_bot import play_match
from game.clubs.club_state import ClubState
from ImageTools.extractors.extractor_club import evaluate_club_pick, extract_necessary_club_info_in_event
from config import logger
import time


def pick_club_event(club_state: ClubState, stop_event):
    event_number = 0
    event_entered = False
    while event_entered == False:
        if stop_event.is_set():
            return False
        if claim_club_rewards():     # Taps the 'Exit Info' button if the screen is in the club-event info screen.
            return False
        check_and_exit_club_info()

        # Resets Event Number when still not in an event when last event is visible
        if check_last_club():
            event_number = 0

        # Swipe up in the clubs section to bring the desired club event into view.
        swipe_up_to_club_event(event_number)

        # Taps the desired club event.
        tap_club_event_number(event_number)
        
        if stop_event.is_set():
            return False        
        
        # Evaluate the club event
        event = evaluate_club_event(event_number)
        if event != False:
            if stop_event.is_set():
                return False
            
            try_club_state_init(club_state, event)
            event_found = try_club(club_state, stop_event)
            if event_found:
                event_entered = True
        else:
            event_number += 1
        if event_number > 20:
            return False
    return True

def try_club_state_init(club_state: ClubState, event)-> None:     
    club_state.reset_game_state()
    club_state.set_active_event(event)
    club_state.set_req_list(event['req_list'])
    club_state.set_club_status('TESTING')
    
    
def check_and_exit_club_info():
    """
    Checks if in club-event info screen and exits if so.

    Taps the 'Exit Info' button if the screen is in the club-event info screen.
    """
    if check_exit_info() and not check_info_icon():
        tap_exit_info()


def swipe_up_to_club_event(event_number: int):
    """
    Swipe up in the clubs section to bring the desired club event into view.

    Args:
        event_number (int): The index of the club event to view. If greater than 2,
        the function will calculate the number of swipes needed to bring the event into view.
    """
    if event_number > 2:
        swipe_up_clubs(event_number // 3)
        logger.debug(f"swiped up {event_number // 3} times")


def tap_club_event_number(event_number: int):
    logger.debug(f"Tapping event {event_number}")

    while not check_go_to_club():
        tap_club_event(event_number % 3)
        time.sleep(0.5)
        #! Maybe remove Not sure yet
        claim_club_rewards()



def  evaluate_active_club_event():
    extracted_dict = extract_necessary_club_info_in_event()
    event = {
        "name": extracted_dict["name"],
        "req_list": extracted_dict["req_list"]
    }
    return event

def evaluate_club_event(event_number=0):
    pick_score, extracted_data = evaluate_club_pick()
    if (pick_score is None or pick_score > 15):
        return False
    
    req_list = extracted_data['req_list']
    
    event = {
    "name": extracted_data["name"],
    "score": pick_score,
    "number": event_number,
    "req_list": req_list,
    }
    return event

def try_club(club_state: ClubState, stop_event):
    tap_play_club()
    time.sleep(2)
    
    if stop_event.is_set():
        return False
    
    if check_play_in_club_page():
        tap_play_in_club()
        time.sleep(2)
        set_sort("ASC")
        time.sleep(2)
        
        if stop_event.is_set():
            return False
        
        event_entered = try_club_event_first_time(club_state, stop_event)
        
        if event_entered:
            return True
        else:
            club_state.reset_problem()
            return False

    else:
        return False
    
    
    
    
def try_club_event_first_time(club_state: ClubState, stop_event):
    if stop_event.is_set():
        return False
    go_button_color = get_go_button_color()
    if go_button_color == "BLUE":
        match_status = blue_go_button()
        if match_status == "MATCH PLAYED":
            club_state.reset_error_count()
            club_state.reset_problem()
            return True
    else:
        match_status = go_button_color
    
    if stop_event.is_set():
        return False
    club_state.set_problem(match_status)
    club_state = fix_problems(club_state, stop_event)
    if club_state.club_status == "FAILED":
        return False
    else:
        return try_club_event_first_time(club_state, stop_event)
    
        
def blue_go_button():
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
    tap_go()
    time.sleep(2)
    can_play = check_play_after_go()
    logger.debug("checking play after go:")
    logger.debug("can play: " + str(can_play))
    if can_play:
        return play_match()
    else:
        return get_after_go_problem()
    