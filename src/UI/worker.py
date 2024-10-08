from PyQt5.QtCore import pyqtSignal, QObject
from src.Utils.Adb.adb_class import AdbClass

class Worker(QObject):
    adb_checked = pyqtSignal(bool, str)
    
    def __init__(self, adb_class: AdbClass):
        super().__init__()
        self.adb_class = adb_class



    def check_adb_connection(self):
        connection = self.adb_class.check_connection()
        if connection:
            self.adb_checked.emit(True, "ADB is online.")
        else:
            self.adb_checked.emit(False, "ADB is offline.")
