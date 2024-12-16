from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
from utils.adb import check_adb_connection, adb_connect
import threading
import time


class TerminalTab(QWidget):
    def __init__(self, worker, main_window, parent=None):
        super().__init__(parent)
        self.worker = worker
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.connect_adb_button = QPushButton('Connect ADB', self)
        self.check_adb_button = QPushButton('Check ADB', self)

        layout.addWidget(self.connect_adb_button)
        layout.addWidget(self.check_adb_button)

        self.setLayout(layout)

        # Signal-slot connections
        self.check_adb_button.clicked.connect(self.check_adb)
        self.connect_adb_button.clicked.connect(self.connect_adb)

    def check_adb(self):
        self.main_window.log("Checking ADB...")
        threading.Thread(target=self.worker.check_adb_connection).start()

    def check_adb_on_startup(self):
        # Check ADB status immediately after UI launch
        adb_connected = check_adb_connection()
        if adb_connected:
            self.update_adb_status(True, "ADB is already connected.")
        else:
            self.update_adb_status(False, "ADB is not connected.")

    def connect_adb(self):
        self.main_window.log("Connecting ADB...")
        is_connected = check_adb_connection()
        if is_connected:
            self.update_adb_status(True, "ADB is already connected.")
        else:
            self.update_adb_status(False, "ADB is not connected.")
            adb_connect()
            time.sleep(1)
            self.main_window.log("Connecting ADB...")
            is_connected = check_adb_connection()
            if is_connected:
                self.update_adb_status(True, "ADB is already connected.")
                self.main_window.log("Connection successful.")
            else:
                self.update_adb_status(False, "ADB is not connected.")
                self.main_window.log("Connection failed.")

    def update_adb_status(self, online, message):
        # Handle ADB status update in the UI
        if online:
            self.main_window.adb_status_label.setText("ADB Status: Online")
            # self.connect_adb_button.setEnabled(False)
        else:
            self.main_window.adb_status_label.setText("ADB Status: Offline")
            # self.connect_adb_button.setEnabled(True)
        self.main_window.log(message)