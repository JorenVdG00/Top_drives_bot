import sys
import threading
import time

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLabel, QVBoxLayout, QWidget, QTabWidget, \
    QToolTip
from functions.windows_terminal_functions import start_waydroid_session, stop_waydroid_session, connect_adb_to_waydroid, \
    check_adb_connection, is_waydroid_running, connect_adb_to_bluestacks
from functions.event_functions import full_event_V2 as full_event, capture_screenshot, swipe
from functions.ad_functions import watch_ads
from functions.resize_functions import calculate_screen_size
from database.read_event_to_db import full_event_reader


def start_bot():
    print("Bot started!")


def stop_bot():
    print("Bot stopped")


waydroid_running = is_waydroid_running()
adb_connection = check_adb_connection()


class Worker(QObject):
    adb_checked = pyqtSignal(bool, str)
    waydroid_running = pyqtSignal(bool, str)

    def check_adb_connection(self):
        connection = check_adb_connection()
        if connection:
            self.adb_checked.emit(True, "ADB is online.")
        else:
            self.adb_checked.emit(False, "ADB is offline.")

class BotUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = Worker()

        self.initUI()
        self.bot_thread = None
        self.stop_event = threading.Event()
        # connect_adb_to_bluestacks()
        self.check_adb_on_startup()

    def initUI(self):
        self.setWindowTitle('Game Bot Manager')
        self.setGeometry(100, 100, 800, 600)

        # Create main layout with tabs
        main_layout = QVBoxLayout()
        tabs = QTabWidget()

        # Terminal tab
        terminal_tab = QWidget()
        terminal_layout = QVBoxLayout()
        self.start_waydroid_button = QPushButton('Start Waydroid Session', self)
        self.stop_waydroid_button = QPushButton('Stop Waydroid Session', self)
        self.connect_adb_button = QPushButton('Connect ADB', self)
        self.check_adb_button = QPushButton('Check ADB', self)
        terminal_layout.addWidget(self.start_waydroid_button)
        terminal_layout.addWidget(self.stop_waydroid_button)
        terminal_layout.addWidget(self.connect_adb_button)
        terminal_layout.addWidget(self.check_adb_button)
        terminal_tab.setLayout(terminal_layout)

        # Event tab
        event_tab = QWidget()
        event_layout = QVBoxLayout()
        self.capture_button = QPushButton('Capture Screenshot', self)
        self.watch_ads_button = QPushButton('Watch Ads', self)
        self.swipe_right_button = QPushButton('Swipe Right Event', self)
        self.swipe_up_button = QPushButton('Swipe Up Event', self)
        self.full_event_button = QPushButton('Full Event', self)
        self.stop_full_event_button = QPushButton('Stop Full Event', self)
        event_layout.addWidget(self.capture_button)
        event_layout.addWidget(self.watch_ads_button)
        event_layout.addWidget(self.swipe_right_button)
        event_layout.addWidget(self.swipe_up_button)
        event_layout.addWidget(self.full_event_button)
        event_layout.addWidget(self.stop_full_event_button)
        event_tab.setLayout(event_layout)

        # Add tabs to tab widget
        tabs.addTab(terminal_tab, "Terminal Functions")
        tabs.addTab(event_tab, "Event Functions")

        # Status and log
        self.status_label = QLabel('Status: Idle', self)
        self.adb_status_label = QLabel('ADB Status: Offline', self)
        if waydroid_running:
            self.waydroid_status_label = QLabel('Waydroid Status: Online', self)
        else:
            self.waydroid_status_label = QLabel('Waydroid Status: Offline', self)
        self.log_area = QTextEdit(self)
        self.log_area.setReadOnly(True)

        main_layout.addWidget(tabs)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.adb_status_label)
        main_layout.addWidget(self.waydroid_status_label)
        main_layout.addWidget(self.log_area)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.check_adb_button.clicked.connect(self.check_adb)

        # Connect the worker signal to the update function
        self.worker.adb_checked.connect(self.update_adb_status)

        # Connect buttons to functions
        self.start_waydroid_button.clicked.connect(self.start_waydroid)
        self.stop_waydroid_button.clicked.connect(self.stop_waydroid)
        self.connect_adb_button.clicked.connect(self.connect_adb)
        self.capture_button.clicked.connect(self.capture_screenshot)
        self.watch_ads_button.clicked.connect(self.watch_ads_event)
        self.swipe_right_button.clicked.connect(self.swipe_right_event)
        self.swipe_up_button.clicked.connect(self.swipe_up_event)
        self.full_event_button.clicked.connect(self.full_event_bot)
        self.stop_full_event_button.clicked.connect(self.stop_full_event_bot)


        connect_adb_to_bluestacks()
        # Initialize status checks
        # self.update_adb_status()
        # self.update_waydroid_status()

    def log(self, message):
        self.log_area.append(message)

    def start_waydroid(self):
        self.log("Starting waydroid session...")
        self.waydroid_status_label.setText('Waydroid Status: Online')
        threading.Thread(target=self._start_waydroid_session).start()

    def _start_waydroid_session(self):
        start_waydroid_session()
        times_checked = 0
        while (not is_waydroid_running() or times_checked == 5):
            time.sleep(3)
            times_checked += 1
        self.update_waydroid_status()
        self.check_adb()

    def stop_waydroid(self):
        self.log("Stopping waydroid session...")
        self.waydroid_status_label.setText('Waydroid Status: Offline')
        threading.Thread(target=self._stop_waydroid_session).start()

    def _stop_waydroid_session(self):
        stop_waydroid_session()
        self.update_waydroid_status()

    def connect_adb(self):
        self.log("Connecting ADB...")
        self.adb_status_label.setText("ADB Status: Connecting")
        threading.Thread(target=self._connect_adb_to_waydroid).start()

    def _connect_adb_to_waydroid(self):
        connect_adb_to_waydroid()
        self.check_adb()

    def check_adb(self):
        self.log("Checking ADB...")
        threading.Thread(target=self.worker.check_adb_connection).start()

    def update_adb_status(self, online, message):
        if online:
            self.adb_status_label.setText("ADB Status: Online")
            self.connect_adb_button.setEnabled(False)
        else:
            self.adb_status_label.setText("ADB Status: Offline")
            self.connect_adb_button.setEnabled(True)
        self.log(message)

    def check_adb_on_startup(self):
        # Check ADB status immediately after UI launch
        adb_connected = check_adb_connection()
        if adb_connected:
            self.update_adb_status(True, "ADB is already connected.")
        else:
            self.update_adb_status(False, "ADB is not connected.")

    def capture_screenshot(self):
        self.log("Capturing screenshot...")
        result = capture_screenshot()
        self.log(result)

    def watch_ads_event(self):
        self.log("Watching ads event...")
        full_event_reader()
    def swipe_right_event(self):
        self.log("Swiping right event...")
        swipe(2000, 400, 1100, 400)

    def swipe_up_event(self):
        self.log("Swiping up event...")
        swipe(2000, 1000, 2000, 300)

    def full_event_bot(self):
        self.log("Starting full event bot...")
        self.stop_event.clear()
        self.bot_thread = threading.Thread(target=self.run_full_event)
        self.bot_thread.start()

    def stop_full_event_bot(self):
        self.log("Stopping full event bot...")
        self.stop_event.set()
        if self.bot_thread is not None:
            self.bot_thread.join()
            self.bot_thread = None
        self.log("Full event bot stopped.")

    def run_full_event(self):
        full_event(self.stop_event)

    def update_waydroid_status(self):
        # Implement Waydroid status check logic here
        waydroid_online = self._is_waydroid_online()
        if waydroid_online:
            self.waydroid_status_label.setText('Waydroid Status: Online')
            QToolTip.setFont(self.waydroid_status_label.font())
            self.waydroid_status_label.setToolTip('Waydroid session is running.')
        else:
            self.waydroid_status_label.setText('Waydroid Status: Offline')
            QToolTip.setFont(self.waydroid_status_label.font())
            self.waydroid_status_label.setToolTip('Waydroid session is not running.')

    def _is_adb_online(self):
        is_adb_online = check_adb_connection()
        if not is_adb_online:
            return False
        return True

    def _is_waydroid_online(self):
        is_waydroid_online = is_waydroid_running()
        print('test', is_waydroid_online)
        if not is_waydroid_online:
            return False
        return True



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BotUI()
    ex.show()
    sys.exit(app.exec_())
