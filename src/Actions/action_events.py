from PIL import Image

from src.Actions.action_base import ActionBase


class ActionEvent(ActionBase):
    def __init__(self):
        super().__init__()
        self._initialize_action_map()

    def tap_prize_card(self, number: int):
        coords = self.get_coords("claim_prizes")
        x1, y1, x_step, y_step = coords
        x = x1 + (x_step * (number % 5))
        y = y1 + (y_step * (number // 5))

        self.cmd_runner.tap(x, y)

    def tap_event(self, number: int):
        if number > 2:
            number = number % 3
        bool = self.tap_action(f'event_{number+1}')
        return bool

    def tap_play_event(self):
        bool = self.tap_action('play_event')
        return bool


    def swipe_left_event(self) -> bool:
        return self.swipe_action('swipe_left_event')

    def _initialize_action_map(self):
        event_actions = {
            'event_1': 'event_1',
            'event_2': 'event_2',
            'event_3': 'event_3',
            'play_event': 'play_event',
            'swipe_left_event': 'swipe_left_event',
        }
        self.action_map.update(event_actions)