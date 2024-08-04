import re
import subprocess


# Change this to the port your adb is listening on
ADB_PORT = 5555
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


if __name__ == '__main__':
    connect_adb_to_waydroid()
