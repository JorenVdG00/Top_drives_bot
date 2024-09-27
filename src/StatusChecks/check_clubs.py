from src.StatusChecks.check_base import CheckBase


class CheckClubs(CheckBase):
    def __init__(self):
        super().__init__()

    def check_club_rewards(self, screenshot=None) -> bool:
        """Checks if club rewards can be collected."""

        if screenshot:
            return self.check_screenshot_for(screenshot, 'club_rewards')
        else:
            return self.check_screen_for('club_rewards')

    def check_play_in_club(self, screenshot=None) -> bool:
        """Checks if in club page can be playe."""

        if screenshot:
            return self.check_screenshot_for(screenshot, 'play_in_club')
        else:
            return self.check_screen_for('play_in_club')

    def check_go_to_club(self, screenshot=None) -> bool:
        """Checks if there is a selected club that can be played."""

        if screenshot:
            return self.check_screenshot_for(screenshot, 'go_to_club')
        else:
            return self.check_screen_for('go_to_club')

    def _initialize_check_map(self):
        club_checks = {
            'club_rewards': 'club_rewards',
            'play_in_club': 'play_in_club',
            'play_club': 'play_club',
        }
        self.check_map.update(club_checks)
