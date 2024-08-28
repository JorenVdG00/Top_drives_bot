# Top_drives_bot

## Description

This is a bot for a mobile card game, Top drives, I spent too much time playing so I thought I should make it play the
game automatically. :)

## Table of Contents

- [Prerequisites](#prerequisites)
- [Game Setup](#Game-Setup)
- [Installation](#installation)
- [Configuration](#configuration)
- [Contributing](#contributing)

## Installation

To get a local copy up and running, follow these steps:

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Waydroid (LINUX)/ Bluestacks(Windows)  #ANDROID EMULATOR#
- adb (android debug bridge)
- Working Top Drives – Car Cards Racing
- OpenCV-Python
- PIL
- pytesseract

### Game-Setup

Find an android emulator where Top Drives works.
I will be using Waydroid for this tutorial.

1. Download [Waydroid](https://docs.waydro.id/usage/install-on-desktops)
2. Download [Waydroid-Script](https://github.com/casualsnek/waydroid_script) to add GApps and easy device certificate
   authorisation
3. Install [ADB](#ADB-Installation)
4. Registrate Device Certificate (**step 2.**)
5. Download the game on google play, If this does not work download it through [aptoide](https://top-drives.en.aptoide.com/app)
6. Test and play the game the bot will work from Events/clubs not the main Campaign. You need to play a bit before you can activate the bot.


#### ADB-Installation

Linux:

1. **Update Package List**

   Open a terminal and update the package list to ensure you have the latest information about available packages.

   ```sh
   sudo apt update
   ```
2. **Install ADB**
   Install ADB by running the following command:
   ```sh
   sudo apt install adb
   ```
3. **Verify Installation**
   ```sh
   adb version
   ```
4. **Connect ADB -> Waydroid**
   First You need to make sure Waydroid is running type:
   ```sh
   Waydroid status
   ```
   Check if the device already has been connected
   ```sh
   adb devices
   ```
   If List is empty
   ```sh
   adb connect (the IP-Address from Waydroid status + :PortNumber)
   ```
   You can set Port through
   ```sh
   adb tcpip 5555
   ```

5. Verify Connection
   ```sh
   adb devices
   ```

   
   






### Installation Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/JorenVdG00/Top_drives_bot.git
    cd Top_drives_bot
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```


#TODO: Complete the read.me
