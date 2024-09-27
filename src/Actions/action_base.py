import time

from src.TopDrives.base_bot import BotBase


class ActionBase(BotBase):
    def __init__(self):
        super().__init__()
        self.action_map = {}
        self._initialize_action_map()

    # BASICS

    def tap(self, name: str) -> bool:
        coords = self.file_utils.get_rand_box_coords(name)
        if coords:
            x, y = coords
            self.cmd_runner.tap(x, y)
            self.logger.success(f"Tapped: {name} at ({x}, {y})")
            return True
        else:
            self.logger.error(f"Coordinates for '{name}' not found in configuration")
            return False

    def swipe(self, name: str) -> bool:
        coords = self.file_utils.get_swipe_coords(name)
        if coords:
            x1, y1, x2, y2 = coords
            self.cmd_runner.swipe(x1, y1, x2, y2)
            self.logger.success(f"Swiped: {name} ... ({x1}, {y1})-->({x2}, {y2})")
            return True
        else:
            self.logger.error(f"Coordinates for '{name}' not found in configuration")
            return False

    def swipe_a_to_b(self, nameA: str, nameB: str) -> bool:
        coordsA = self.file_utils.get_rand_box_coords(nameA)
        coordsB = self.file_utils.get_rand_box_coords(nameB)
        if coordsA and coordsB:
            xA, yA = coordsA
            xB, yB = coordsB
            self.cmd_runner.swipe(xA, yA, xB, yB)
            self.logger.success(f"Swiped: {nameA}-->{nameB} ... ({xA}, {yA})-->({xB}, {yB})")
            return True
        else:
            self.logger.error(f'Coordinates for {nameA} and {nameB} not found in configuration')
            return False

    def tap_action(self, action_name: str) -> bool:
        coord_name = self.action_map.get(action_name)
        if coord_name:
            return self.tap(coord_name)
        else:
            self.logger.error(f"No coordinates found for action: {action_name}")
            return False

    def swipe_action(self, action_name: str) -> bool:
        coord_name = self.action_map.get(action_name)
        if coord_name:
            return self.swipe(coord_name)
        else:
            self.logger.error(f"No coordinates found for action: {action_name}")
            return False

    # COMMON TAPS

    def tap_home(self) -> bool:
        return self.tap_action('home')

    def tap_events(self) -> bool:
        return self.tap_action('events')

    def tap_go(self) -> bool:
        return self.tap_action('go')

    def tap_play_after_go(self):
        return self.tap_action('play_after_go')

    def tap_skip_match(self):
        return self.tap_action('skip')

    def tap_accept_skip(self):
        return self.tap_action('skip_accept')

    def tap_claim_event(self):
        self.tap_action('claim_event')
        time.sleep(2)
        for i in range(10):
            self.tap_action('claim_event')
            time.sleep(1)
        time.sleep(5)

    def tap_upgrade_after_match(self):
        return self.tap_action('upgrade_after_match')

    def tap_sort_button(self):
        return self.tap_action('sort')

    def tap_sort_rq(self):
        return self.tap_action('sort_rq')

    def tap_req_tab(self):
        return self.tap_action('req_tab')

    def tap_req_1(self):
        return self.tap_action('req_1')

    def tap_req_2(self):
        return self.tap_action('req_2')

    def tap_reset_hand(self):
        return self.tap_action('reset_hand')

    def tap_add_to_hand(self):
        return self.tap_action('add_to_hand')

    def tap_exit_car(self):
        return self.tap_action('exit_car')

    # SWIPES

    def swipe_left_cars(self) -> bool:
        return self.swipe_action('swipe_left_cars')

    def unswipe_slots(self) -> bool:
        try:
            self.swipe_a_to_b('hand_1', 'garage_1_2')
            time.sleep(0.2)
            self.swipe_a_to_b('hand_2', 'garage_1_2')
            time.sleep(0.2)
            self.swipe_a_to_b('hand_3', 'garage_1_2')
            time.sleep(0.2)
            self.swipe_a_to_b('hand_4', 'garage_1_2')
            time.sleep(0.2)
            self.swipe_a_to_b('hand_5', 'garage_1_2')
            time.sleep(0.2)
        finally:
            return True

    def swipe_cars_to_slots_in_match(self, assignments: list[int] = None) -> bool:
        """
        Swipe cars into the slots, optionally based on a list of assignments.
        If no assignments are given, cars will be swiped in slot order (1-5).
        """
        self.logger.debug('swiping cars to slots')
        if assignments is None:
            assignments = list(range(1, 6))  # Default swipe 1-5 cars

        for slot_nr, car in enumerate(assignments, start=1):
            self.logger.debug(f'swiping car {car} to slot {slot_nr}')
            self.swipe_a_to_b(f'ingame_car{car}', f'ingame_slot{slot_nr}')
        return True

    def _initialize_action_map(self):
        """
        Initialize and update the check_map with predefined actions.
        This method is intended to be called during the object initialization
        to populate the check_map with common checks.
        """
        base_actions = {
            'home': 'home',
            'events': 'events',
            'go': 'go_button',
            'play_after_go': 'play_after_go',
            'skip': 'skip',
            'skip_accept': 'skip_accept',
            'upgrade_after_match': 'upgrade_after_match',
            'claim_event': 'claim_event',
            'sort': 'sort_button',
            'sort_rq': 'sort_rq',
            'req_tab': 'requirements_tab',
            'req_1': 'requirements_1',
            'req_2': 'requirements_2',
            'unswipe_slots': 'unswipe_slots',
            'unswipe_step': 'unswipe_to_car',
            'garage_1_1': 'garage_1_1',
            'garage_2_1': 'garage_2_1',
            'garage_3_1': 'garage_3_1',
            'garage_1_2': 'garage_1_2',
            'garage_2_2': 'garage_2_2',
            'garage_3_2': 'garage_3_2',
            'ingame_car1': 'ingame_car1',
            'ingame_car2': 'ingame_car2',
            'ingame_car3': 'ingame_car3',
            'ingame_car4': 'ingame_car4',
            'ingame_car5': 'ingame_car5',
            'ingame_slot1': 'ingame_slot1',
            'ingame_slot2': 'ingame_slot2',
            'ingame_slot3': 'ingame_slot3',
            'ingame_slot4': 'ingame_slot4',
            'ingame_slot5': 'ingame_slot5',
            'reset_hand': 'reset_hand',
            'add_to_hand': 'add_to_hand',
            'exit_car': 'exit_car'
        }
        self.action_map.update(base_actions)

    # @staticmethod
    # def get_rand_box_coords(name: str) -> tuple[int, int] | None:
    #     coords = get_rand_box_coords(name)
    #     return (coords)
    #
    # @staticmethod
    # def get_coords(name: str) -> tuple[int, int, int, int] | None:
    #     coords = get_coords(name)
    #     return coords
