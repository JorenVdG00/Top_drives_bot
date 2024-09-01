from PyQt5.QtCore import pyqtSignal, QObject
from UI.functions.windows_terminal_functions import check_adb_connection
class Worker(QObject):
    adb_checked = pyqtSignal(bool, str)

    def check_adb_connection(self):
        connection = check_adb_connection()
        if connection:
            self.adb_checked.emit(True, "ADB is online.")
        else:
            self.adb_checked.emit(False, "ADB is offline.")
