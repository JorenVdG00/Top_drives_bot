import time

from src.TopDrives.base_bot import BotBase
from src.Actions.action_base import ActionBase
from src.StatusChecks.check_base import CheckBase


class GameBotBase(BotBase):
    def __init__(self):
        super().__init__()
        self.actions = ActionBase()
        self.checks = CheckBase()
        self.bot_state = None

    def go_to_event_page(self):
        self.actions.tap_home()
        self.actions.tap_events()

    def set_game_state(self, bot_state):
        self.bot_state = bot_state

    def get_bot_state(self):
        return self.bot_state

    def claim_event(self):
        can_claim, double_check = True, True
        while can_claim and double_check:
            with self.screen_manager.screenshot_context as screenshot:
                can_claim = self.checks.check_event_ended(screenshot)
                if can_claim:
                    double_check = self.checks.check_double_check(screenshot)
                    if double_check:
                        self.actions.tap_claim_event()

    def tap_go_and_play(self) -> str:
        go_button_color = self.checks.get_go_button_color()
        self.logger.debug(f'go_button_color: {go_button_color}')
        if go_button_color == 'BLUE':
            self.logger.debug('Tapping GO-BUTTON and checking for problems')
            self.actions.tap_go()
            time.sleep(1)
            if self.checks.check_play_after_go():
                self.actions.tap_play_after_go()
                return 'PLAY'
            else:
                status = self.checks.get_after_go_problem()
                return status
        elif go_button_color == 'RED':
            self.logger.debug('go_button_color: RED, RQ too high')
            return 'HIGH_RQ'
        elif go_button_color == 'GRAY':
            self.logger.debug('go_button_color: GRAY, MISSING CARS')
            return 'MISSING_CARS'
        else:
            self.logger.debug(f'No Button Found')
            return 'NONE'

    def skip_match(self):
        while not self.checks.check_accept_skip():
            self.actions.tap_skip_match()
            time.sleep(3)

        self.actions.tap_accept_skip()
        for _ in range(5):
            self.actions.tap_skip_match()
        if self.checks.check_upgrade_after_match():
            self.actions.tap_upgrade_after_match()


    def fix_after_go_problem(self):
        pass
