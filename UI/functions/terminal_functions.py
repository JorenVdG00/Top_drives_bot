import re
import subprocess

# Change this to the port your adb is listening on
ADB_PORT = 5555


def start_waydroid_session():
    try:
        process = subprocess.Popen(['waydroid', 'session', 'start'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True)
        return process
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None


def stop_waydroid_session():
    try:
        result = subprocess.run(['waydroid', 'session', 'stop'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        if result.returncode != 0:
            print(f"Error running waydroid stop: {result.stderr}")
            return None
        return result.stdout
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None


def get_waydroid_status():
    try:
        result = subprocess.run(['waydroid', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Error running waydroid status: {result.stderr}")
            return None
        return result.stdout
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None


def is_waydroid_running():
    status_output = get_waydroid_status()
    if 'RUNNING' in status_output:
        return True
    else:
        return False


def extract_ip_address(status_output):
    ip_pattern = re.compile(r'IP address:\s+(\d+\.\d+\.\d+\.\d+)')
    match = ip_pattern.search(status_output)
    if match:
        return match.group(1)
    else:
        print("IP address not found in waydroid status output.")
        return None


def adb_connect(ip_address):
    try:
        adb_command = ['adb', 'connect', f'{ip_address}:{ADB_PORT}']
        result = subprocess.run(adb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Error running adb connect: {result.stderr}")
        else:
            print(result.stdout)
    except Exception as e:
        print(f"Exception occurred: {e}")


def connect_adb_to_waydroid():
    status_output = get_waydroid_status()
    if status_output:
        ip_address = extract_ip_address(status_output)
        if ip_address:
            adb_connect(ip_address)


def adb_devices():
    try:
        adb_command = ['adb', 'devices']
        result = subprocess.run(adb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Error running adb devices: {result.stderr}")
            return None
        else:
            print(result.stdout)
            return result.stdout
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None


def check_adb_connection():
    status = adb_devices()
    ip_address = extract_ip_address(get_waydroid_status())
    if ip_address:
        if status:
            if ip_address in status:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


if __name__ == '__main__':
    connect_adb_to_waydroid()
