from src.StatusChecks.check_base import CheckBase


class CheckClubs(CheckBase):
    def __init__(self):
        super().__init__()
        super()._initialize_check_map()
        self._initialize_check_map()

    def check_club_rewards(self, screenshot=None) -> bool:
        """Checks if club rewards can be collected."""
        self.logger.debug("Checking if club rewards can be collected...")
        return self.check_element("club_rewards", screenshot)


    def check_play_in_club_page(self, screenshot=None) -> bool:
        """Checks if in club page can be playe."""
        return self.check_element("play_in_club", screenshot, tolerance=25)


    def check_go_to_club(self, screenshot=None) -> bool:
        """Checks if there is a selected club that can be played."""
        return self.check_element("go_to_club", screenshot)

    def check_info_icon(self, screenshot=None) -> bool:
        """Checks if there is not a selected club now there is a info icon."""
        return self.check_element("info_icon", screenshot)

    def check_exit_info(self, screenshot=None) -> bool:
        """Checks if accidently pressed on info icon."""
        return self.check_element("exit_info", screenshot)
                                  
    def _initialize_check_map(self):
        club_checks = {
            'club_rewards': 'club_rewards',
            'play_in_club': 'play_in_club',
            'play_club': 'play_club',
            'info_icon': 'info_icon',
            'exit_info': 'exit_info',
        }
        self.check_map.update(club_checks)
