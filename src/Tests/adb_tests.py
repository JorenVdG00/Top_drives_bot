import logging
import os

from src.Utils.Adb.adb_class import AdbClass
from src.Utils.ImageTools.resize_class import ResizeClass
from src.Utils.Adb.adb_connector import adb_connect # NOT USING ANYMORE

from dotenv import load_dotenv

ADB_IP = os.getenv('ADB_IP')
ADB_PORT = os.getenv('ADB_PORT')

logger = logging.getLogger(__name__)
resize = ResizeClass(logger)

adbTestObject = AdbClass(ADB_IP, ADB_PORT, logger, resize)

def test_adb_class():
    connection = adbTestObject.check_connection()
    print(connection)
    print('try to connect')
    adbTestObject.adb_connector.adb_connect()
    connection = adbTestObject.check_connection()
    print(f'Connection: {connection}')
