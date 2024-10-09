from src.Actions.action_base import ActionBase
import time

class ActionClub(ActionBase):
    def __init__(self):
        super().__init__()
        super()._initialize_action_map()
        self._initialize_action_map()
        for index, key in enumerate(self.action_map.keys()):
            print(index, key)

    def tap_clubs(self):
        self.tap_action("clubs")

    def tap_claim_club_reward(self):
        self.tap_action("claim_clubs")

    def tap_play_in_club(self):
        self.tap_action("play_in_club")

    def tap_play_club(self):
        self.tap_action("play_club")

    def tap_club_event(self, number: int):
        """number should start from 0"""
        if number > 2:
            number = number % 3
        self.tap_action(f"club_event_{number+1}")

    def tap_back_club(self):
        self.tap_action("back_club")

    def swipe_up_clubs(self, times:int = 1):
        for _ in range(times):
            self.swipe_and_hold_action("swipe_up_clubs")
            time.sleep(0.5)

    def tap_garage_car(self, garage_x, garage_y):
        self.tap_action(f"garage_{garage_x}_{garage_y}")
        
    def tap_exit_info(self):
        self.tap_action("exit_info")

    def add_cars_to_hand(self):
        self.tap_action("add_to_hand")

    def _initialize_action_map(self):
        club_actions = {
            "clubs": "clubs",
            "claim_clubs": "claim_clubs",
            "play_in_club": "play_in_club",
            "play_club": "play_club",
            "club_event_1": "club_event_1",
            "club_event_2": "club_event_2",
            "club_event_3": "club_event_3",
            "back_club": "back_club",
            "swipe_up_clubs": "swipe_up_clubs",
            "add_to_hand": "add_to_hand",
            "garage_1_1": "garage_1_1",
            "garage_1_2": "garage_1_2",
            "garage_2_1": "garage_2_1",
            "garage_2_2": "garage_2_2",
            "garage_3_1": "garage_3_1",
            "garage_3_2": "garage_3_2",
            "exit_info": "exit_info",
        }
        self.action_map.update(club_actions)
