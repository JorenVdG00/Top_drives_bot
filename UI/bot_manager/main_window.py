from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget, QLabel, QTextEdit
from terminal_tab import TerminalTab
from event_tab import EventTab
from car_assignment_tab import CarAssignmentTab
from worker import Worker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = Worker()
        self.initUI()
        self.setupConnections()

    def initUI(self):
        self.setWindowTitle('Game Bot Manager')
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_layout = QVBoxLayout()
        tabs = QTabWidget()

        # Add tabs
        terminal_tab = TerminalTab(self.worker, self)
        event_tab = EventTab(self)
        car_assignment_tab = CarAssignmentTab(self)

        tabs.addTab(terminal_tab, "Terminal Functions")
        tabs.addTab(event_tab, "Event Functions")
        tabs.addTab(car_assignment_tab, "Car Assignment")

        # Status and log
        self.adb_status_label = QLabel('ADB Status: Offline', self)
        self.log_area = QTextEdit(self)
        self.log_area.setReadOnly(True)

        # Finalize layout
        container = QWidget()
        main_layout.addWidget(tabs)
        main_layout.addWidget(self.adb_status_label)
        main_layout.addWidget(self.log_area)
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def setupConnections(self):
        # Connect the worker signal to the update function
        self.worker.adb_checked.connect(self.update_adb_status)

    def update_adb_status(self, online, message):
        # Handle ADB status update in the UI
        if online:
            self.adb_status_label.setText("ADB Status: Online")
            # self.connect_adb_button.setEnabled(False)
        else:
            self.adb_status_label.setText("ADB Status: Offline")
            # self.connect_adb_button.setEnabled(True)
        self.log(message)

    def log(self, message):
        # Log messages to the log area
        self.log_area.append(message)
