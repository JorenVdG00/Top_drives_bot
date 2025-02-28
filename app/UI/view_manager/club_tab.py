from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from game.clubs.club_game_bot import play_club_events
from app.utils.ImageTools.image_utils import capture_screenshot
import threading


class ClubTab(QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.stop_event = threading.Event()  # Add an event to signal stopping
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.capture_button = QPushButton('Capture Screenshot', self)
        self.play_clubs_button = QPushButton('Play Clubs', self)
        self.stop_clubs_button = QPushButton('Stop Clubs', self)  # Stop button

        
        layout.addWidget(self.capture_button)
        layout.addWidget(self.play_clubs_button)
        layout.addWidget(self.stop_clubs_button)
     
        self.setLayout(layout)
        
        
        self.capture_button.clicked.connect(self.capture_screenshot)
        self.play_clubs_button.clicked.connect(self.start_clubs_bot)
        self.stop_clubs_button.clicked.connect(self.stop_clubs_bot)  # Connect stop button


    def capture_screenshot(self):
        self.main_window.log("Capturing screenshot...")
        result = capture_screenshot()
        self.main_window.log(result)
        
    def start_clubs_bot(self):
        self.main_window.log("Starting clubs bot...")
        self.stop_event.clear()  # Reset the stop event
        self.bot_thread = threading.Thread(target=self.run_clubs_bot, daemon=True)
        self.bot_thread.start()
        
    def stop_clubs_bot(self):
        self.main_window.log("Stopping clubs bot...")
        self.stop_event.set()  # Signal the thread to stop
            
    def run_clubs_bot(self):
        play_club_events(self.stop_event)