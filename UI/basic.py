import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLabel, QVBoxLayout, QWidget
from UI.functions.event_functions import full_event_V2 as full_event  # Ensure your full_event function is modified to check for the stop signal
from UI.functions.general_functions import capture_screenshot, swipe
from functions.terminal_functions import connect_adb_to_waydroid
def start_bot():
    print("Bot started!")


def stop_bot():
    print("Bot stopped")

class BotUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.bot_thread = None  # Initialize bot_thread attribute
        self.stop_event = threading.Event()  # Initialize stop_event attribute

    def initUI(self):
        self.setWindowTitle('Game Bot Manager')
        self.setGeometry(100, 100, 800, 600)

        # Create widgets
        self.start_button = QPushButton('Start Bot', self)

        self.stop_button = QPushButton('Stop Bot', self)
        self.capture_button = QPushButton('Capture Screenshot', self)
        self.swipe_right_button = QPushButton('Swipe Right Event', self)
        self.swipe_up_button = QPushButton('Swipe Up Event', self)
        self.full_event_button = QPushButton('Full Event', self)
        self.stop_full_event_button = QPushButton('Stop Full Event', self)  # Add Stop Full Event button
        self.status_label = QLabel('Status: Idle', self)
        self.log_area = QTextEdit(self)
        self.log_area.setReadOnly(True)

        # Connect buttons to functions
        self.start_button.clicked.connect(self.start_bot)
        self.stop_button.clicked.connect(self.stop_bot)
        self.capture_button.clicked.connect(self.capture_screenshot)
        self.swipe_right_button.clicked.connect(self.swipe_right_event)
        self.swipe_up_button.clicked.connect(self.swipe_up_event)
        self.full_event_button.clicked.connect(self.full_event_bot)
        self.stop_full_event_button.clicked.connect(self.stop_full_event_bot)  # Connect Stop Full Event button

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.capture_button)
        layout.addWidget(self.swipe_right_button)
        layout.addWidget(self.swipe_up_button)
        layout.addWidget(self.full_event_button)
        layout.addWidget(self.stop_full_event_button)  # Add Stop Full Event button to layout
        layout.addWidget(self.status_label)
        layout.addWidget(self.log_area)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def log(self, message):
        self.log_area.append(message)

    def start_bot(self):
        self.log("Starting bot...")
        self.status_label.setText("Status: Running")
        threading.Thread(target=start_bot).start()

    def stop_bot(self):
        self.log("Stopping bot...")
        self.status_label.setText("Status: Stopped")
        stop_bot()

    def capture_screenshot(self):
        self.log("Capturing screenshot...")
        result = capture_screenshot()
        self.log(result)

    def swipe_right_event(self):
        self.log("Swiping right event...")
        swipe(2000, 400, 1100, 400)

    def swipe_up_event(self):
        self.log("Swiping up event...")
        swipe(2000, 1000, 2000, 300)

    def full_event_bot(self):
        self.log("Starting full event bot...")
        # Clear the stop event and start the thread
        self.stop_event.clear()
        self.bot_thread = threading.Thread(target=self.run_full_event)
        self.bot_thread.start()

    def stop_full_event_bot(self):
        self.log("Stopping full event bot...")
        self.stop_event.set()  # Set the stop event
        if self.bot_thread is not None:
            self.bot_thread.join()  # Wait for the thread to finish
            self.bot_thread = None
        self.log("Full event bot stopped.")

    def run_full_event(self):
        full_event(self.stop_event)  # Pass the stop_event to full_event function


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BotUI()
    ex.show()
    sys.exit(app.exec_())
