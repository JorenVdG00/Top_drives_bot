import sys
from PyQt5.QtWidgets import QApplication, QDialog
from UI.view_manager.main_window import MainWindow
from UI.view_manager.config_check import ConfigDialog, check_config  # Import the config check functions and dialog

def main():
    app = QApplication(sys.argv)

    # Check if configuration exists
    if not check_config():
        config_dialog = ConfigDialog()
        if config_dialog.exec_() != QDialog.Accepted:
            sys.exit(0)  # Exit if the user cancels the configuration dialog

    # If configuration is set, proceed to show the main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
