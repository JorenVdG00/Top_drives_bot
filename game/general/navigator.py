import time
from game.clubs.club_actions import tap_clubs
from game.general.general_actions import tap_home, tap_events
from game.general.claim_events import claim_event


def go_to_club_page():
    go_to_event_page()
    time.sleep(1)
    tap_clubs()
    time.sleep(1)
    
def go_to_event_page():
    tap_home()
    time.sleep(1)
    tap_events()
    time.sleep(1)
    claim_event()
    time.sleep(1)