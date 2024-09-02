from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from UI.functions.event_functions import full_event_V2 as full_event, capture_screenshot, swipe
from UI.functions.ad_functions import watch_ads
from database.read_event_to_db import full_event_reader
import threading


class EventTab(QWidget):
    def __init__(self,main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.capture_button = QPushButton('Capture Screenshot', self)
        self.watch_ads_button = QPushButton('Watch Ads', self)
        self.swipe_right_button = QPushButton('Swipe Right Event', self)
        self.swipe_up_button = QPushButton('Swipe Up Event', self)
        self.full_event_button = QPushButton('Full Event', self)
        self.stop_full_event_button = QPushButton('Stop Full Event', self)

        layout.addWidget(self.capture_button)
        layout.addWidget(self.watch_ads_button)
        layout.addWidget(self.swipe_right_button)
        layout.addWidget(self.swipe_up_button)
        layout.addWidget(self.full_event_button)
        layout.addWidget(self.stop_full_event_button)

        self.setLayout(layout)

        # Signal-slot connections
        self.capture_button.clicked.connect(self.capture_screenshot)
        self.watch_ads_button.clicked.connect(self.watch_ads_event)
        self.swipe_right_button.clicked.connect(self.swipe_right_event)
        self.swipe_up_button.clicked.connect(self.swipe_up_event)
        self.full_event_button.clicked.connect(self.full_event_bot)
        # self.stop_full_event_button.clicked.connect(self.stop_full_event_bot)

    def capture_screenshot(self):
        self.main_window.log("Capturing screenshot...")
        result = capture_screenshot()
        self.main_window.log(result)

    def watch_ads_event(self):
        self.main_window.log("Watching ads event...")
        full_event_reader()

    def swipe_right_event(self):
        self.main_window.log("Swiping right event...")
        swipe(2000, 400, 1100, 400)

    def swipe_up_event(self):
        self.main_window.log("Swiping up event...")
        swipe(2000, 1000, 2000, 300)

    def full_event_bot(self):
        self.main_window.log("Starting full event bot...")
        # self.stop_event.clear()
        self.bot_thread = threading.Thread(target=self.run_full_event)
        self.bot_thread.start()

    def stop_full_event_bot(self):
        self.main_window.log("Stopping full event bot...")
        # self.stop_event.set()
        if self.bot_thread is not None:
            self.bot_thread.join()
            self.bot_thread = None
        self.main_window.log("Full event bot stopped.")

    def run_full_event(self):
        full_event() #ADD self.stop_event
