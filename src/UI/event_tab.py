from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
# from OLD.UI.functions.general_game_functions import swipe_left_cars
# from OLD.UI.functions.event_functions import full_event_V2 as full_event, capture_screenshot
# from OLD.UI.functions.clubs_functions import swipe_clubs_3_up, full_clubs
# from OLD.UI.functions.resize_functions import calculate_screen_size
# from OLD.Database.read_event_to_db import full_event_reader
from src.Game.club_bot import ClubBot
from src.UI.worker import Worker
# from src.UI.main_window import MainWindow
import threading


class EventTab(QWidget):
    def __init__(self, main_window: 'MainWindow', parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.bot = self.main_window.bot
        self.resizer = self.bot.resizer
        self.club_bot = ClubBot()
        self.stop_event = threading.Event()
        self.initUI()
        self.resizer.calculate_screen_size()

    def initUI(self):
        layout = QVBoxLayout()

        self.capture_button = QPushButton('Capture Screenshot', self)
        self.watch_ads_button = QPushButton('Watch Ads', self)
        self.swipe_right_button = QPushButton('Swipe Right Event', self)
        self.swipe_up_button = QPushButton('Swipe Up Event', self)
        self.full_event_button = QPushButton('Full Event', self)
        self.full_clubs_button = QPushButton('Full Clubs', self)
        self.stop_full_clubs_button = QPushButton('Stop Full clubs', self)

        layout.addWidget(self.capture_button)
        layout.addWidget(self.watch_ads_button)
        layout.addWidget(self.swipe_right_button)
        layout.addWidget(self.swipe_up_button)
        layout.addWidget(self.full_event_button)
        layout.addWidget(self.full_clubs_button)
        layout.addWidget(self.stop_full_clubs_button)

        self.setLayout(layout)

        # Signal-slot connections
        self.capture_button.clicked.connect(self.capture_screenshot)
        # self.watch_ads_button.clicked.connect(self.watch_ads_event)
        # self.swipe_right_button.clicked.connect(self.swipe_right_event)
        # self.swipe_up_button.clicked.connect(self.swipe_up_event)
        # self.full_event_button.clicked.connect(self.full_event_bot)
        self.full_clubs_button.clicked.connect(self.full_clubs_bot)
        # self.stop_full_event_button.clicked.connect(self.stop_full_event_bot)

    def capture_screenshot(self):
        self.main_window.log("Capturing screenshot...")
        result = self.bot.screen_manager.capture_screenshot()
        self.main_window.log(result)

    # def watch_ads_event(self):
    #     self.main_window.log("Watching ads event...")
    #     full_event_reader()

    # def swipe_right_event(self):
    #     self.main_window.log("Swiping right event...")
    #     swipe_left_cars()

    # def swipe_up_event(self):
    #     self.main_window.log("Swiping up event...")
    #     swipe_clubs_3_up()

    # def full_event_bot(self):
    #     self.main_window.log("Starting full event bot...")
    #     # self.stop_event.clear()
    #     self.bot_thread = threading.Thread(target=self.run_full_event)
    #     self.bot_thread.start()

    def full_clubs_bot(self):
        self.main_window.log("Starting full clubs bot...")
        self.stop_event.clear()
        self.bot_thread = threading.Thread(target=self.run_full_clubs)
        self.bot_thread.start()

    def stop_full_clubs_bot(self):
        self.main_window.log("Stopping full event bot...")
        self.stop_event.set()
        if self.bot_thread is not None:
            self.bot_thread.join()
            self.bot_thread = None
        self.main_window.log("Club bot stopped.")
        
        
    # def stop_full_event_bot(self):
    #     self.main_window.log("Stopping full event bot...")
    #     # self.stop_event.set()
    #     if self.bot_thread is not None:
    #         self.bot_thread.join()
    #         self.bot_thread = None
    #     self.main_window.log("Full event bot stopped.")

    # def run_full_event(self):
    #     full_event()  # ADD self.stop_event

    def run_full_clubs(self):
        self.club_bot.play_clubs(self.stop_event)