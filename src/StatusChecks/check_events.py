from src.StatusChecks.check_base import CheckBase

class CheckEvents(CheckBase):
    def __init__(self):
        super().__init__()
        self._initialize_check_map()

    # Prize Star Checks
    def check_prize_star_1(self, screenshot=None) -> bool:
        """Checks if the first prize star is present."""

        if screenshot:
            return self.check_screenshot_for(screenshot, 'prize_star_1')
        else:
            return self.check_screen_for('prize_star_1')

    def check_prize_star_2(self, screenshot=None) -> bool:
        """Checks if the second prize star is present."""

        if screenshot:
            return self.check_screenshot_for(screenshot, 'prize_star_2')
        else:
            return self.check_screen_for('prize_star_2')

    def check_prize_star_3(self, screenshot=None) -> bool:
        """Checks if the third prize star is present."""

        if screenshot:
            return self.check_screenshot_for(screenshot, 'prize_star_3')
        else:
            return self.check_screen_for('prize_star_3')

    # Prize Card Checks
    def check_prize_card_start(self, screenshot=None) -> list[int]:
        prize_cards_left = []

        start_coords, target_color = self.get_color_coords('prize_card_start')
        step_coords, _ = self.get_color_coords('prize_card_step')

        if start_coords:
            if screenshot is None:
                with self.screen_manager.screenshot_context() as screenshot:
                    resized_img = self.resizer.resize_img(screenshot)
            else:
                img = self.image_utils.open_image(screenshot)
                resized_img = self.resizer.resize_img(img)
                self.image_utils.close_image(img)

            prize_cards_left = [
                i for i in range(15)
                if resized_img.getpixel((
                    start_coords[0] + (i % 5) * step_coords[0],
                    start_coords[1] + (i // 5) * step_coords[1]
                )) == target_color
            ]

        else:
            self.logger.debug(f'No prize card coords found')
        return prize_cards_left

    # Ticket Checks
    def check_ticket(self, screenshot=None) -> bool:
        """Checks if a ticket is available."""
        if screenshot:
            return self.check_screenshot_for(screenshot, 'ticket')
        else:
            return self.check_screen_for('ticket')

    def check_empty_ticket(self, screenshot=None) -> bool:
        """Checks if the ticket slot is empty."""
        if screenshot:
            return self.check_screenshot_for(screenshot, 'empty_ticket')
        else:
            return self.check_screen_for('empty_ticket')

    # Event Requirements Not Met
    def check_event_reqs_not_met(self, screenshot=None) -> bool:
        """Checks if event requirements are not met."""
        if screenshot:
            return self.check_screenshot_for(screenshot, 'event_reqs_not_met')
        else:
            return self.check_screen_for('event_reqs_not_met')

    def _initialize_check_map(self):
        event_checks = {
            'event_1': 'event_1',
            'event_2': 'event_2',
            'event_3': 'event_3',
            'available_event_1': 'available_event_1',
            'available_event_2': 'available_event_2',
            'available_event_3': 'available_event_3',
            'unavailable_event': 'unavailable_event',
            'unavailable_last_visible': 'unavailable_last_visible',
            'no_last_visible': 'no_last_visible',
            'event_reqs_not_met': 'event_reqs_not_met',
            'prize_star_1': 'prize_star_1',
            'prize_star_2': 'prize_star_2',
            'prize_star_3': 'prize_star_3',
            'prize_card_start': 'prize_card_start',
            'prize_card_step': 'prize_card_step',
            'ticket': 'ticket',
            'empty_ticket': 'empty_ticket',
        }
        self.check_map.update(event_checks)