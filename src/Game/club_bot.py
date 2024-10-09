from src.Game.game_bot_base import GameBotBase
from src.Actions.action_clubs import ActionClub
from src.StatusChecks.check_clubs import CheckClubs
from src.Utils.ImageTools.Extractor.extractor_club import ExtractorClub
import time
import threading
from collections import Counter
from typing import Optional





class GameBotClub(GameBotBase):
    def __init__(self):
        super().__init__()
        self.actions = ActionClub()
        self.checks = CheckClubs()
        self.problem_fixer = ProblemFixer(self)
        self.picker = EventPicker(self)
        self.active_event = None
        self.played_matches = 0
        self.club_status = None

    def set_active_event(self, event):
        self.active_event = event
        self.club_status = "playing"
        self.played_matches += 1

    def played_match(self):
        self.played_matches += 1

    def remove_active_event(self):
        self.active_event = None
        self.club_status = None
        self.played_matches = 0

    def get_active_event(self):
        return self.active_event
    

    def go_to_club_page(self) -> None:
        """
        Go to the club page.
        From anywhere THat you can go to home.
        
        """
        self.logger.debug("Going to club page")
        self.go_to_event_page()
        time.sleep(5)
        self.claim_event()
        time.sleep(0.5)
        self.actions.tap_clubs()
        

    def fill_hand_slots(self, req_list: Optional[list[int]]):
        """
        Fills the hand with the required number of cars based on the req_list.

        Args:
            req_list (Optional[list[int]]): A list of required car counts.
                                            It can have one or two integers indicating how many cars to add for each request.
        """
        # Validate if req_list has values
        if not req_list or len(req_list) == 0:
            return

        # Assign the first request count (req1_count) and initialize req2_count as None
        req1_count = req_list[0]
        req2_count = req_list[1] if len(req_list) > 1 else None
        time.sleep(0.5)
        # Switch to the first request
        self.actions.tap_req_tab()
        time.sleep(1)
        # If there's a second request, handle accordingly
        if req2_count is not None:
            if req1_count + req2_count > 5:
                # When the combined car count exceeds 5
                self.actions.tap_req_1()
                time.sleep(0.5)
                self.actions.tap_req_2()
                time.sleep(0.5)
                self.actions.tap_req_tab()
                time.sleep(0.5)
                # Fill the second request first
                self.add_from_garage(req2_count)
                time.sleep(1)
                # Go back and switch to the first request to fill the remaining slots
                self.actions.tap_req_tab()
                time.sleep(0.5)
                self.actions.tap_req_2()
                time.sleep(0.5)
                self.actions.tap_req_tab()
                time.sleep(0.5)
                self.add_from_garage(5 - req2_count)
            else:
                # When combined car count is 5 or fewer
                self.actions.tap_req_1()
                time.sleep(0.5)
                self.actions.tap_req_tab()
                time.sleep(0.5)
                self.add_from_garage(req1_count)
                time.sleep(0.5)

                # Switch to the second request
                self.actions.tap_req_tab()
                time.sleep(1)
                self.actions.tap_req_1()
                time.sleep(0.5)
                self.actions.tap_req_2()
                time.sleep(0.5)
                self.actions.tap_req_tab()
                time.sleep(0.5)
                self.add_from_garage(req2_count)
        else:
            # Single request handling
            self.add_from_garage(req1_count)

    def add_car_to_hand(self, tries: int = 1) -> bool:
        """
        Tries to add a car to the hand based on the current attempt number.

        Args:
            tries (int): The number of tries attempted to add a car.

        Returns:
            bool: True if the car is successfully added, False otherwise.
        """
        # Swipe left after every 6 tries
        if tries % 6 == 0:
            self.actions.swipe_left_cars()

        # Calculate which car to tap
        nr = tries if tries // 6 <= 1 else tries % 6
        x = (nr // 2) + 1
        y = 2 if nr % 2 == 0 else 1

        # Interact with the car
        self.actions.tap_garage_car(x, y)
        time.sleep(0.5)
        # Check if the car can be added to hand
        can_add = self.checks.check_add_to_hand()
        is_fusing = self.checks.check_is_fusing()
        if can_add and not is_fusing:
            self.actions.tap_add_to_hand()
            return True
        else:
            self.actions.tap_exit_car()
            time.sleep(0.5)
            return False

    def add_from_garage(self, number_of_cars: int, start_spot: int = 1) -> bool:
        """
        Adds cars from the garage to available slots.

        Args:
            number_of_cars (int): The number of cars to add to the hand.
            tries (int, optional): The number of tries to find and add a car. Defaults to 1.

        Returns:
            bool: True if cars are successfully added, False if there are not enough missing slots or an error occurs.
        """
        # Check initial missing slots
        missing_slots = self.checks.check_missing_slots()
        missing_slots_count = len(missing_slots)

        # If there are fewer missing slots than needed, return False (can't fill more than available)
        if number_of_cars > missing_slots_count:
            return False

        cars_added = 0

        while cars_added < number_of_cars:
            time.sleep(0.5)
            # Try to add car from the garage to the hand
            if self.add_car_to_hand(start_spot):
                cars_added += 1
            start_spot += 1

        # Check if we still have missing slots after adding the cars
        remaining_missing_slots = self.checks.check_missing_slots()

        if missing_slots_count == len(remaining_missing_slots) + number_of_cars:
            return True
        else:
            if missing_slots_count < len(remaining_missing_slots) + number_of_cars:
                for _ in range(
                    len(remaining_missing_slots) + number_of_cars - missing_slots_count
                ):
                    while not self.add_car_to_hand(start_spot):
                        start_spot += 1
                if missing_slots_count == len(remaining_missing_slots) + number_of_cars:
                    return True
                else:
                    return False
            else:
                return False

    def claim_club_rewards(self) -> bool:
        """
        Claims the rewards for the active club event if available.

        Returns:
            bool: True if rewards were claimed, False otherwise.
        """
        if self.checks.check_club_rewards():
            self.logger.debug("Claiming club rewards...")
            self.actions.tap_claim_club_reward()
            self.remove_active_event()
            return True
        return False

    def play_active_event(self) -> bool:
        while self.played_matches < 34:
            if self.claim_club_rewards():
                return False
            if self.checks.check_go_to_club():
                self.actions.tap_play_club()
            if self.checks.check_play_in_club_page():
                self.actions.tap_play_in_club()
                time.sleep(0.5)
                if self.tap_go_and_play():
                    self.played_matches += 1
                else:
                    self.club_status = "problem"
                    return False
            else:
                return False
        self.club_status = "Maxed out"
        return True

    def tap_blue_go_button(self) -> bool:
        """Tap the blue go button in the club event page and play the match.

        Tap the go button, check if match possible to be played, if so, play the match.
        If play not appears check problem, fix problem and try-again and return False.

        Returns:
            bool: True if the match was played, False otherwise.
        """
        self.logger.debug("Tapping GO-BUTTON and checking for problems")

        self.actions.tap_go()
        time.sleep(4)
        if self.checks.check_play_after_go():
            
            self.play_match()
            return True
        else:
            time.sleep(1)
            self.problem_fixer.fix_after_go_problem()
            return self.problem_fixer.test_and_play_go()

    def tap_red_go_button(self) -> None:
        """
        Remove all cars from hand, and put new according to reqList.

        Returns:
            bool: False as the match was not played.
        """
        self.logger.debug("go_button_color: RED, RQ too high")
        self.actions.unswipe_slots()
        self.fix_missing_slots()

    def tap_gray_go_button(self) -> None:
        """
        If go-button color is GRAY, it means that some cars are missing in hand.
        This function will check missing slotnumber, and refill the hand with cars according to reqList.

        Returns:
            None
        """

        self.logger.debug("go_button_color: GRAY, MISSING CARS")
        missing_slots = self.checks.check_missing_slots()
        for nr in missing_slots:
            self.actions.unswipe_slots(nr)
        self.fix_missing_slots()

    def tap_go_and_play(self) -> bool:
        loop_count = 0
        while True:
            loop_count += 1
            if loop_count > 5:
                return False
            go_button_color = self.checks.get_go_button_color()
            self.logger.debug(f"go_button_color: {go_button_color}")
            if go_button_color == "BLUE":
                self.logger.debug("Tapping GO-BUTTON and checking for problems")
                if self.tap_blue_go_button():
                    return True
                else:
                    return False

            elif go_button_color == "RED":
                self.logger.debug("fixing Red-BUTTON")
                self.tap_red_go_button()
                continue

            elif go_button_color == "GRAY":
                self.logger.debug("fixing GRAY-BUTTON")
                self.tap_gray_go_button()
                continue

            else:
                self.logger.debug(f"No Button Found")
                return False

    def play_match(self):
        self.actions.tap_play_after_go()
        time.sleep(4)
        # self.actions.swipe_cars_to_slots_in_match()
        self.logger.debug("CHecking for reset hand")
        while self.checks.check_reset_hand():
            time.sleep(3)
            self.logger.debug("swiping cars to slots in match")
            self.actions.swipe_cars_to_slots_in_match()
            time.sleep(2)
        self.skip_match()
        for _ in range(2):
            self.actions.tap_back_club()
            time.sleep(1)


    def fix_missing_slots(self):
        missing_slots = self.checks.check_missing_slots()
        req_list = self.active_event["req_list"]
        if len(missing_slots) > 0:
            if sum(req_list) > 5:
                if req_list[1] < min(missing_slots):
                    self.actions.tap_req_tab()
                    time.sleep(0.5)
                    self.actions.tap_req_1()
                    time.sleep(0.5)
                    self.actions.tap_req_tab()
                    time.sleep(0.5)
                    self.add_from_garage(len(missing_slots))
                elif req_list[1] > max(missing_slots):
                    self.actions.tap_req_tab()
                    time.sleep(0.5)
                    self.actions.tap_req_1()
                    time.sleep(0.5)
                    self.actions.tap_req_2()
                    time.sleep(0.5)
                    self.actions.tap_req_tab()
                    time.sleep(0.5)
                    self.add_from_garage(len(missing_slots))
                else:
                    under_req2 = [x for x in missing_slots if x < req_list[1]]
                    self.actions.tap_req_tab()
                    time.sleep(0.5)
                    self.actions.tap_req_1()
                    time.sleep(0.5)
                    self.actions.tap_req_2()
                    time.sleep(0.5)
                    self.actions.tap_req_tab()
                    time.sleep(0.5)
                    self.add_from_garage(len(under_req2))

                    self.actions.tap_req_tab()
                    time.sleep(0.5)
                    self.actions.tap_req_2()
                    time.sleep(0.5)
                    self.actions.tap_req_tab()
                    time.sleep(0.5)
                    self.add_from_garage(len(missing_slots) - len(under_req2))

            else:
                if req_list[1] == 0:
                    self.actions.tap_req_tab()
                    self.add_from_garage(len(missing_slots))
                else:
                    self.actions.tap_req_tab()
                    under_req1 = [x for x in missing_slots if x < req_list[0]]
                    self.actions.tap_req_1()
                    time.sleep(0.5)
                    self.actions.tap_req_tab()
                    time.sleep(0.5)
                    self.add_from_garage(len(under_req1))

                    self.actions.tap_req_tab()
                    time.sleep(0.5)
                    self.actions.tap_req_1()
                    time.sleep(0.5)
                    self.actions.tap_req_2()
                    time.sleep(0.5)
                    self.actions.tap_req_tab()
                    time.sleep(0.5)
                    self.add_from_garage(len(missing_slots) - len(under_req1))

        # if len(missing_slots) > 0:

    # def fix_problem_after_go(self, req_list):
    #     problem_status = self.checks.get_after_go_problem()
    #     if problem_status == "EVENT_ENDED":
    #         self.go_to_event_page()
    #         time.sleep(0.5)
    #         self.claim_event()
    #         time.sleep(0.5)
    #         self.actions.tap_clubs()
    #         self.claim_club_rewards()
    #         return False
    #     elif problem_status == "CARS_SERVICING":
    #         slot_numbers = self.checks.check_repair_slots()
    #         for nr in slot_numbers:
    #             self.actions.unswipe_slots(nr)
    #         self.fix_missing_slots()
    #         return True
    #     elif problem_status == "REQUIREMENTS":
    #         self.actions.unswipe_slots()
    #         self.fill_hand_slots(req_list)
    #         return True
    #     else:
    #         self.logger.error("Error while trying club OTHER")
    #         return False

    

class ProblemFixer:
    def __init__(self, game_bot: GameBotClub):
        self.game = game_bot
        self.logger = self.game.logger
        
    # GET PROBLEMS
    def get_go_problem(self):
        return self.game.checks.get_after_go_problem()

    def get_go_color(self):
        return self.game.checks.get_go_button_color()

    # AFTER GO
    def fix_after_go_problem(self):
        problem = self.get_go_problem()
        time.sleep(1)
        # Random_tap to get out of problem_screen
        self.game.actions.close_problem_after_go()
        time.sleep(0.5)

        if problem == "EVENT_ENDED":
            self.fix_event_ended()
            return False

        elif problem == "CARS_SERVICING":
            self.fix_cars_servicing()

        elif problem == "REQUIREMENTS":
            self.fix_reqs()

        else:
            self.game.logger.error("Error while trying club OTHER")
            return False

        return True

    def test_and_play_go(self) -> bool:
        test_loops = 0
        while test_loops < 5:
            self.game.actions.tap_go()
            time.sleep(4)
            if self.game.checks.check_play_after_go():
                time.sleep(0.5)
                self.game.play_match()
                return True
            else:
                if self.fix_after_go_problem():
                    test_loops += 1
                    continue
                else:
                    return False
        self.game.logger.error("Error stuck in a loop")
        return False

    def fix_event_ended(self):
        self.game.go_to_event_page()
        time.sleep(0.5)
        self.game.claim_event()
        time.sleep(0.5)
        self.game.actions.tap_clubs()
        self.game.claim_club_rewards()

    def fix_cars_servicing(self):
        slot_numbers = self.game.checks.check_repair_slots()
        for nr in slot_numbers:
            self.game.actions.unswipe_slots(nr)
        self.game.fix_missing_slots()

    def fix_reqs(self):
        self.game.actions.unswipe_slots()
        
        self.logger.debug("req_list: " + str(self.game.active_event["req_list"]))
        req_list = self.game.active_event["req_list"]
        # self.game.fill_hand_slots(req_list)
        self.game.fix_missing_slots()

    # GO COLOR PROBLEMS

    def fix_go_color(self, color: str):
        if color == "GRAY":
            self.game.fix_missing_slots()
        elif color == "RED":
            self.game.actions.unswipe_slots()
            self.game.fix_missing_slots()


class EventPicker:
    def __init__(self, game_bot: GameBotClub):
        self.game = game_bot
        self.logger = self.game.logger
        self.extractor = ExtractorClub(self.game)
        self.best_event = {"name": None, "score": 20000, "number": 0}
        self.current_number = 0

    def set_best_event(self, best_event):
        self.best_event = best_event

    def compare_best_event(self, best_event):
        if self.best_event["score"] > best_event["score"]:
            self.best_event = best_event

    def find_worthy_event(self):
        number = 0
        play_best = False
        while self.game.active_event == None:
            if self.game.stop_event.is_set():
                return False
            with self.game.screen_manager.screenshot_context() as screenshot:
                if not self.game.checks.check_info_icon(screenshot) and self.game.checks.check_exit_info(screenshot):
                    self.game.actions.tap_exit_info()
                    
            if play_best:
                number = self.best_event["number"]
            if number > 2:
                self.game.actions.swipe_up_clubs(number // 3)
                self.logger.debug(f"swiped up {number // 3} times")
                
            self.logger.debug(f"Tapping event {number}")
            while not self.game.checks.check_go_to_club():
                self.game.actions.tap_club_event((number % 3) + 1)
                time.sleep(0.5)
                self.game.claim_club_rewards()
            
            event = self.evaluate_club_event()
            if event != False or play_best:
                self.game.set_active_event(event)
                time.sleep(0.5)
                has_active = self.try_club()
                if has_active:
                    # self.set_active_event(event)
                    return True
                else:
                    play_best = False
                    self.game.remove_active_event()
            # NOT WORTHY EVENT
            if number == 12:
                play_best = True
                number = 0
                self.game.go_to_club_page()
            else:
                number += 1
            self.game.actions.tap_back_club()


    def evaluate_club_event(self):
        pick_score, extracted_data = self.extractor.evaluate_club_pick()
        req_list = self.extractor.get_req_list(extracted_data)

        event = {
            "name": extracted_data["name"],
            "score": pick_score,
            "number": self.current_number,
            "req_list": req_list,
        }

        if pick_score < 15:
            return event
        elif pick_score is None:
            return False
        else:
            self.compare_best_event(event)
            return False

    def try_club(self) -> bool:
        self.game.actions.tap_play_club()
        time.sleep(2)

        # Checking play-button is clickable in club-event
        if self.game.checks.check_play_in_club_page():
            self.game.actions.tap_play_in_club()
            time.sleep(2)
            self.game.set_sort("ASC")
            if self.game.tap_go_and_play():
                return True
            else:
                return False
            
        else:
            self.game.go_to_club_page()
            return False


class ClubBot(GameBotClub):
    def __init__(self):
        super().__init__()
        self.extractor = ExtractorClub(self)
        self.bot_status = "Null"
        self.bot_running = False
        
    def play_clubs(self, stop_event: threading.Event):
        self.stop_event = stop_event
        
        self.logger.debug("Club-bot started")
        self.go_to_club_page()
        
        
        time.sleep(2)
        
        self.claim_club_rewards()
        if self.active_event == None and self.checks.check_go_to_club():
            self.actions.tap_play_club()
            self.active_event = self.extractor.extract_necessary_club_info_in_event()
            
        while True:
            if self.stop_event.is_set():
                break
            while self.active_event:
                if self.claim_club_rewards():
                    break
                if self.stop_event.is_set():
                    self.logger.debug("Club-bot stopped")
                    break
                if self.active_event:
                    # PLAY CLUBS TILL MAXED|PROBLEM|END
                    if not self.play_active_event():
                        active = False
                        self.go_to_club_page()
            if self.picker.find_worthy_event():
                continue
        
        

    
