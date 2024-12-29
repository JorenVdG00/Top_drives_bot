from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget, QLabel, QTextEdit, QAction
from UI.view_manager.terminal_tab import TerminalTab
# from UI.view_manager.Not_YET_USING.event_tab import EventTab
# from UI.view_manager.Not_YET_USING.car_assignment_tab_v2 import CarAssignmentTab
from UI.view_manager.club_tab import ClubTab
from UI.view_manager.config_check import ConfigDialog
from UI.view_manager.worker import Worker
from dotenv import load_dotenv
from config import adb_ip, adb_port, ADB_SERIAL_CMD
from utils.adb import calculate_screen_size, adb_connect

import os
load_dotenv()

#!!TESTS
from game.general.general_actions import swipe_left_cars
from game.general.general_checks import get_nr_available_cars, get_nav_title, check_is_fusing
from game.clubs.club_actions import swipe_up_clubs



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = Worker()
        self.initUI()
        self.setupConnections()

    def initUI(self):
        adb_connect()
        calculate_screen_size()
        self.setWindowTitle('Game Bot Manager')
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_layout = QVBoxLayout()
        tabs = QTabWidget()
        menubar = self.menuBar()

        # Add a Settings menu
        settings_menu = menubar.addMenu('Settings')
        test_menu = menubar.addMenu('Test')

        # Add an action to open the configDialog
        config_action = QAction('Configure ADB', self)
        config_action.triggered.connect(self.open_config_dialog)
        settings_menu.addAction(config_action)

        test_action = QAction('Test ADB', self)
        test_action.triggered.connect(self.show_test_dialog)
        test_menu.addAction(test_action)
        
        test_swipe_left_cars = QAction('Test Swipe Left Cars', self)
        test_swipe_left_cars.triggered.connect(self.test_swipe_left_cars)
        test_menu.addAction(test_swipe_left_cars)
        
        test_swipe_up_clubs = QAction('Test Swipe up clubs', self)
        test_swipe_up_clubs.triggered.connect(self.test_swipe_up_clubs)
        test_menu.addAction(test_swipe_up_clubs)
        
        test_available_cars = QAction('Test Available Cars', self)
        test_available_cars.triggered.connect(self.test_available_cars)
        test_menu.addAction(test_available_cars)

        test_nav_title = QAction('Test Nav Title', self)
        test_nav_title.triggered.connect(self.test_nav_title)
        test_menu.addAction(test_nav_title)
        # Add tabs
        terminal_tab = TerminalTab(self.worker, self)
        club_tab = ClubTab(self)
        # event_tab = EventTab(self)
        # car_assignment_tab = CarAssignmentTab(self)

        tabs.addTab(terminal_tab, "Terminal Functions")
        tabs.addTab(club_tab, "Event Functions")
        # tabs.addTab(car_assignment_tab, "Car Assignment")

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

    def open_config_dialog(self):   
        config_dialog = ConfigDialog()
        config_dialog.exec_()

    def show_test_dialog(self):
        adb_ip_env = os.getenv('ADB_IP')
        adb_port_env = os.getenv('ADB_PORT')
        adb_path_env = os.getenv('ADB_PATH')
        self.log(f"Connecting to {adb_ip_env}:{adb_port_env}\n{adb_path_env}")
        self.log(f"2.0. Connecting to {adb_ip}:{adb_port}\n{ADB_SERIAL_CMD}")

    
    def test_swipe_left_cars(self):
        self.log("Swiping left cars...")
        
        swipe_left_cars()
        self.log("Swiping left cars completed.")
        
    def test_swipe_up_clubs(self):
        self.log("Swiping up clubs...")
        
        swipe_up_clubs(1)
        self.log("Swiping up clubs completed.")
        
    def test_available_cars(self):
        self.log("Checking available cars...")
        available_amount = get_nr_available_cars()
        self.log("Available cars: " + str(available_amount))
        
    def test_nav_title(self):
        self.log("Checking nav title...")
        nav_title = check_is_fusing()
        self.log("is_fusing: " + str(nav_title))