import sys
import os
from config import BASE_DIR, reload_env
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import QSettings


class ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_existing_settings()

    def initUI(self):
        self.setWindowTitle("Configuration Settings")
        layout = QVBoxLayout()

        self.adb_ip_label = QLabel("ADB IP:")
        self.adb_ip_input = QLineEdit(self)
        layout.addWidget(self.adb_ip_label)
        layout.addWidget(self.adb_ip_input)

        self.adb_port_label = QLabel("ADB Port:")
        self.adb_port_input = QLineEdit(self)
        layout.addWidget(self.adb_port_label)
        layout.addWidget(self.adb_port_input)

        self.adb_path_label = QLabel("Path to adb executable:")
        self.adb_path_input = QLineEdit(self)
        layout.addWidget(self.adb_path_label)
        layout.addWidget(self.adb_path_input)

        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_adb_path)
        layout.addWidget(self.browse_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def load_existing_settings(self):
        # Load existing settings using QSettings
        settings = QSettings("TopDrivesBot", "TopDrivesBotConfig")
        adb_ip = settings.value("ADB_IP", "")
        adb_port = settings.value("ADB_PORT", "")
        adb_path = settings.value("ADB_PATH", "")

        # Pre-fill the input fields with the existing settings
        self.adb_ip_input.setText(adb_ip)
        self.adb_port_input.setText(adb_port)
        self.adb_path_input.setText(adb_path)

    def browse_adb_path(self):
        file_dialog = QFileDialog()
        adb_path, _ = file_dialog.getOpenFileName(self, "Select adb executable")
        if adb_path:
            self.adb_path_input.setText(adb_path)

    def save_settings(self):
        adb_ip = self.adb_ip_input.text()
        adb_port = self.adb_port_input.text()
        adb_path = self.adb_path_input.text()

        adb_dir_path = os.path.dirname(adb_path)

        if not adb_ip or not adb_port or not adb_path:
            QMessageBox.warning(self, "Missing Information", "Please provide all the required settings.")
            return

        # Save settings using QSettings
        settings = QSettings("TopDrivesBot", "TopDrivesBotConfig")
        settings.setValue("ADB_IP", adb_ip)
        settings.setValue("ADB_PORT", adb_port)
        settings.setValue("ADB_PATH", adb_dir_path)

        update_env(adb_ip=adb_ip, adb_port=adb_port, adb_path=adb_dir_path)
        reload_env()

        self.accept()


def check_config():
    settings = QSettings("TopDrivesBot", "TopDrivesBotConfig")
    adb_ip = settings.value("ADB_IP")
    adb_port = settings.value("ADB_PORT")
    adb_path = settings.value("ADB_PATH")

    if not adb_ip or not adb_port or not adb_path:
        return False

    return True


def update_env(adb_ip=None, adb_port=None, adb_path=None):
    env_path = os.path.join(BASE_DIR, '.env')

    # Load existing lines from the .env file
    with open(env_path, "r") as file:
        lines = file.readlines()

    # Dictionary to track which settings are updated
    updates = {
        'ADB_IP': adb_ip,
        'ADB_PORT': adb_port,
        'ADB_PATH': adb_path
    }

    # Update the lines with new values
    with open(env_path, "w") as file:
        for line in lines:
            key = line.split('=')[0]
            if key in updates and updates[key] is not None:
                file.write(f"{key}={updates[key]}\n")
                updates[key] = None  # Mark as updated
            else:
                file.write(line)

        # Add any new settings that were not in the file
        for key, value in updates.items():
            if value is not None:
                file.write(f"{key}={value}\n")
