import os
from src.Utils.terminal_helper import run_subprocess_from_path, set_cwd
from dotenv import load_dotenv

load_dotenv()

ADB_PORT = os.getenv('ADB_PORT')


def adb_connect(ip_address):
    set_cwd()
    adb_cmd = f"adb connect {ip_address}:{ADB_PORT}"
    run_subprocess_from_path(adb_cmd)


def connect_adb_to_game():
    ip_address = os.getenv('ADB_IP')
    adb_connect(ip_address)


def adb_devices():
    adb_devices_cmd = "adb devices"
    output = run_subprocess_from_path(adb_devices_cmd)
    return output


def check_adb_connection():
    output = adb_devices()
    if ADB_PORT in output:
        return True
    else:
        print("ADB connection failed")
        return False