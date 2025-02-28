import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from config import ADB_SERIAL_CMD, BASIC_WIDTH, BASIC_HEIGHT, BOT_SCREENSHOTS_DIR, logger, resize_values, adb_ip, adb_port
from app.utils.os_utils import set_cwd
from utils.coords_utils import CoordsUtils


load_dotenv()

WINDOWS_ADB_PATH = os.getenv('ADB_PATH')
coords_utils = CoordsUtils


def run_subprocess_from_path(command: str, path: str = WINDOWS_ADB_PATH) -> str | None:
    """
    Run a subprocess command from the specified path and return the output.

    Args:
        command (str): The command to run.
        path (str): The path to run the command in. Default is WINDOWS_ADB_PATH.

    Returns:
        str | None: The standard output from the command or None if there is an error.
    """
    try:
        process = subprocess.Popen(command, cwd=path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True)
        stdout, stderr = process.communicate()

        if stdout:
            logger.debug(stdout)
            return stdout
        if stderr:
            logger.error(f'Error occurred performing {command}, No Exception:\n {stderr}')
    except Exception as e:
        logger.error(f'Error occurred performing {command}:\n {e}')
    return None


def set_ip_address(ip_address: str):
    ip_address = ip_address

def set_port(port: str):
    port = port
    
def reload_adb_connector():
    adb_connect()
    connection = check_adb_connection()



def adb_connect():
    """
    Connect ADB to the specified IP address and port.
    """
    set_cwd()
    adb_cmd = f"adb connect {adb_ip}:{adb_port}"
    output = run_subprocess_from_path(adb_cmd)

    # Check if the connection succeeded based on the output
    if "connected" in output or "already connected" in output:
        logger.info(f"Successfully connected to {adb_ip}:{adb_port}")
        calculate_screen_size()
        logger.info(f"resize_values: {resize_values}")
    else:
        logger.error(f"Failed to connect to {adb_ip}:{adb_port}")



def adb_devices() -> str:
    """
    Get the list of devices connected via ADB.

    Returns:
        str: A list of devices connected to ADB.
    """
    adb_devices_cmd = "adb devices"
    output = run_subprocess_from_path(adb_devices_cmd)
    return output

def check_adb_connection() -> bool:
    """
    Check if the ADB connection is established by verifying if the device is listed.

    Returns:
        bool: True if the device is connected, False otherwise.
    """
    output = adb_devices()
    if adb_port in output:
        logger.info(f"ADB is connected to {adb_ip}:{adb_port}")
        return True
    else:
        logger.error("ADB connection failed")
        return False




def calculate_screen_size():
    global resize_values
    set_cwd()
    command = f"{ADB_SERIAL_CMD} shell wm size"
    size_result = run_subprocess_from_path(command)
    print(size_result)
    if size_result == None:
        # adb_connect()
        # return calculate_screen_size()
        return [1.0, 1.0]
    size = size_result.strip()
    print("size: " + size)
    print("size_result: " + str(size_result))
    # Parse the size information
    if "Physical size: " in size:
        size = size.split("Physical size: ")[1]
        width, height = map(int, size.split("x"))
        print(f"Width: {width}, Height: {height}")
        resize_value = [width / BASIC_WIDTH, height / BASIC_HEIGHT]
        print(resize_value)
        resize_values[:] = resize_value
        print(f'resize_values with : >\{resize_values}<')
        return resize_value
