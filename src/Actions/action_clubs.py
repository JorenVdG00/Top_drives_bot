from src.Actions.action_base import ActionBase


class ActionClub(ActionBase):
    def __init__(self):
        super().__init__()
        self._initialize_action_map()

    def tap_clubs(self):
        self.tap_action('clubs')

    def tap_claim_club_reward(self):
        self.tap_action('claim_clubs')

    def tap_play_in_club(self):
        self.tap_action('play_in_club')

    def tap_play_club(self):
        self.tap_action('play_club')

    def tap_play_club_event(self, number:int):
        """number should start from 0"""
        if number > 2:
            number = number % 3
        self.tap_action(f'club_event_{number+1}')

    def tap_back_club(self):
        self.tap_action('back_club')

    def swipe_up_clubs(self):
        self.swipe_action('swipe_up_clubs')

    def add_cars_to_hand(self, number_of_cars: int):
        for garage_nr, slot_nr



    def _initialize_action_map(self):
        club_actions = {
            'clubs': 'clubs',
            'claim_clubs': 'claim_clubs',
            'play_in_club': 'play_in_club',
            'play_club': 'play_club',
            'club_event_1': 'club_event_1',
            'club_event_2': 'club_event_2',
            'club_event_3': 'club_event_3',
            'back_club': 'back_club',
            'swipe_up_clubs': 'swipe_up_clubs',
        }
        self.action_map.update(club_actions)
