from src.Game.game_bot_base import GameBotBase
from src.Actions.action_clubs import ActionClub
from src.StatusChecks.check_clubs import CheckClubs
from src.Utils.ImageTools.Extractor.extractor_club import ExtractorClub
import time


class ClubBot(GameBotBase):
    def __init__(self):
        super().__init__()
        self.club_count = 0
        self.current_hand = None


class GameBotClub(GameBotBase):
    def __init__(self):
        super().__init__()
        self.actions = ActionClub()
        self.checks = CheckClubs()

    def add_cars_to_hand(self, req_list):
        pass


class ChoosingEvent(GameBotClub):
    def __init__(self):
        super().__init__()
        self.extractor = ExtractorClub()
        self.best_event = {'name': None, 'score': 20000, 'number': 0}
        self.current_number = 0

    def set_best_event(self, best_event):
        self.best_event = best_event

    def compare_best_event(self, best_event):
        if self.best_event['score'] > best_event['score']:
            self.best_event = best_event

    def evaluate_club(self):
        pick_score, extracted_data = self.extractor.evaluate_club_pick()
        if pick_score < 15:
            return extracted_data
        elif pick_score is None:
            return False
        else:
            event = {'name': extracted_data['name'], 'score': pick_score, 'number': self.current_number}
            self.compare_best_event(event)
            return False

    def try_club(self, req_list):
        self.actions.tap_play_club()
        time.sleep(0.5)

        # Checking play-button is clickable in club-event
        if self.checks.check_play_in_club():
            self.actions.tap_play_in_club()
            time.sleep(0.5)

            # Get color of go-button
            go_button_color = self.checks.get_go_button_color()

            # CLICK GO if go-button BLUE
            if go_button_color == 'BLUE':
                self.actions.tap_go()
                time.sleep(0.5)
                if self.checks.check_play_after_go():
                    self.actions.tap_play_after_go()
                    time.sleep(0.5)
                    self.actions.swipe_cars_to_slots_in_match()
                    time.sleep(0.5)
                    self.skip_match()
                    return True
                else:
                    problem_status = self.checks.get_after_go_problem()
                    if problem_status == 'EVENT_ENDED':
                        self.go_to_event_page()
                        time.sleep(0.5)
                        self.claim_event()
                        time.sleep(0.5)
                        self.actions.tap_clubs()
                    elif problem_status == 'CARS_REPAIR':
                        pass
                        # TODO: FIX_REPAIR_HAND
                        # self.fix_repair_hand()
                    else:
                        self.logger.error("Error while trying club OTHER")
                    return False

            elif go_button_color == 'GRAY':
                missing_cars = self.checks.check_missing_slots_start()  # LIST OF BOOLS TRUE OR FALSE  TRUE==MISSING
