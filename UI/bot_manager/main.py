import sys
from PyQt5.QtWidgets import QApplication, QDialog
from main_window import MainWindow
from config_check import ConfigDialog, check_config  # Import the config check functions and dialog

if __name__ == '__main__':
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
