from PIL import Image
import os
import random
from datetime import datetime
import time
import subprocess
from config import BOT_SCREENSHOTS_DIR


basic_width = 2210
basic_height = 1248

global resize_values  # Declare global variable


def resize_coordinate(value, resize_factor):
    return int(value * resize_factor)


def resize_same_factor(value1: int, value2: int, resize_factor: float):
    return int(value1 * resize_factor), int(value2 * resize_factor)


def resize_coordinates(x: int, y: int, resize_factor: list):
    return resize_coordinate(x, resize_factor[0]), resize_coordinate(y, resize_factor[1])


def resize_ranges(x1: int, x2: int, y1: int, y2: int, resize_factor: list):
    return (resize_coordinate(x1, resize_factor[0]), resize_coordinate(x2, resize_factor[0]),
            resize_coordinate(y1, resize_factor[1]), resize_coordinate(y2, resize_factor[1]))


def tap(x, y):
    os.system(f"adb shell input tap {x} {y}")


def swipe(x1, y1, x2, y2):
    os.system(f"adb shell input swipe {x1} {y1} {x2} {y2}")


def capture_screenshot():
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # Construct the screenshot filename
    filename = f"{BOT_SCREENSHOTS_DIR}/screenshot_{timestamp}.png"
    # Take the screenshot
    os.system("adb shell screencap -p /sdcard/screenshot.png")
    os.system("adb pull /sdcard/screenshot.png " + filename)
    os.system("adb shell rm /sdcard/screenshot.png")
    print(f"Screenshot saved to {filename}")
    return filename


def calculate_screen_size():
    global resize_values
    size_result = subprocess.run("adb shell wm size", shell=True, capture_output=True, text=True)
    size = size_result.stdout.strip()
    print("size: " + size)
    print("size_result: " + str(size_result))
    # Parse the size information
    if "Physical size: " in size:
        size = size.split("Physical size: ")[1]
        width, height = map(int, size.split("x"))
        print(f"Width: {width}, Height: {height}")
        resize_values = [width / basic_width, height / basic_height]
        return resize_values


def check_ticket(img_path):
    print("checking ticket")
    img = Image.open(img_path)
    x, y = resize_coordinates(890, 1150, resize_values)
    color = img.getpixel((x, y))
    if color == (248, 171, 23, 255):
        print(color)
        print("Ticket found!")
        return True
    else:
        print('No ticket found')
        return False


def check_empty_ticket(img_path):
    print("checking empty ticket")
    img = Image.open(img_path)
    empty_ticket_color = (146, 146, 146, 255)
    x, y = resize_coordinates(890, 1150, resize_values)

    color = img.getpixel((x, y))
    if color == empty_ticket_color:
        print(color)
        print("empty Ticket found!")
        return True
    else:
        print('No ticket found')
        return False


def tap_event(event_number: int = 1):
    print("tapping event")
    y1, y2 = resize_coordinate(400, resize_values[1]), resize_coordinate(800, resize_values[1])
    y = random.randint(y1, y2)
    if event_number == 1:
        x1, x2 = resize_coordinate(840, resize_values[0]), resize_coordinate(1180, resize_values[0])
        x = random.randint(x1, x2)
    elif event_number == 2:
        x1, x2 = resize_coordinate(1480, resize_values[0]), resize_coordinate(1890, resize_values[0])
        x = random.randint(x1, x2)
    elif event_number == 3:
        x1, x2 = resize_coordinate(2000, resize_values[0]), resize_coordinate(2150, resize_values[0])
        x = random.randint(x1, x2)
    else:
        x1, x2 = resize_coordinate(2000, resize_values[0]), resize_coordinate(2150, resize_values[0])
        x = random.randint(x1, x2)
    tap(x, y)
    time.sleep(3)


def check_event_available(event_number: int = 1):
    unavailable_color = (112, 112, 112, 255)
    screenshot = capture_screenshot()
    if event_number == 3:
        img = Image.open(screenshot)
        x, y = resize_coordinates(1978, 285, resize_values)
        color = img.getpixel((x, y))
        if color == unavailable_color:
            print("event not available")
            return False
        else:
            print("event available")
            return True


def tap_play_event():
    print("tapping play event")
    x1, x2, y1, y2 = resize_ranges(1700, 1800, 1110, 1200, resize_values)
    rand_tap = (random.randint(x1, x2),
                random.randint(y1, y2))
    tap(rand_tap[0], rand_tap[1])
    time.sleep(2)


def check_cannot_play():
    print("checking cannot play")
    cannot_play_color = (51, 51, 51, 255)
    selected_hand_fault_color = (27, 31, 40, 255)
    selected_hand_fault_coords = (490, 815)
    img_path = capture_screenshot()
    img = Image.open(img_path)
    x, y = resize_coordinates(720, 750, resize_values)
    color1 = img.getpixel((x, y))
    x, y = resize_coordinates(selected_hand_fault_coords[0], selected_hand_fault_coords[1], resize_values)
    color2 = img.getpixel((x, y))
    remove_screenshot(img_path)
    print(color1, color2)
    if color1 == cannot_play_color or color2 == selected_hand_fault_color:
        print("cannot play found!")
        return True
    else:
        print('cannot play not found')
        return False


def tap_events():
    print("tapping events")
    x1, x2, y1, y2 = resize_ranges(920, 1280, 280, 470, resize_values)
    rand_tap = (random.randint(x1, x2),
                random.randint(y1, y2))
    tap(rand_tap[0], rand_tap[1])
    time.sleep(3)


def tap_go_button_event():
    print("tapping go button")
    x1, x2, y1, y2 = resize_ranges(1930, 2040, 1050, 1090, resize_values)
    rand_tap = (random.randint(x1, x2),
                random.randint(y1, y2))
    tap(rand_tap[0], rand_tap[1])
    time.sleep(2)


def tap_in_event_play():
    print("tapping in event play")
    x1, x2, y1, y2 = resize_ranges(1000, 1200, 830, 900, resize_values)
    rand_tap = (random.randint(x1, x2),
                random.randint(y1, y2))
    tap(rand_tap[0], rand_tap[1])
    time.sleep(5)


def swipe_cars_to_slots():
    print("swiping cars to slots")
    y1, y2 = resize_same_factor(1110, 1150, resize_values[1])
    y_car = random.randint(y1, y2)
    car1 = random.randint(int(490 * resize_values[0]), int(520 * resize_values[0]))
    car2 = random.randint(int(880 * resize_values[0]), int(920 * resize_values[0]))
    car3 = random.randint(int(1280 * resize_values[0]), int(1300 * resize_values[0]))
    car4 = random.randint(int(1560 * resize_values[0]), int(1600 * resize_values[0]))
    car5 = random.randint(int(1900 * resize_values[0]), int(1930 * resize_values[0]))

    race_slot_y = random.randint(int(700 * resize_values[1]), int(800 * resize_values[1]))
    race_slot1 = random.randint(int(200 * resize_values[0]), int(300 * resize_values[0]))
    race_slot2 = random.randint(int(610 * resize_values[0]), int(700 * resize_values[0]))
    race_slot3 = random.randint(int(1050 * resize_values[0]), int(1150 * resize_values[0]))
    race_slot4 = random.randint(int(1460 * resize_values[0]), int(1570 * resize_values[0]))
    race_slot5 = random.randint(int(1880 * resize_values[0]), int(2000 * resize_values[0]))

    # TODO: add logic for race slots

    swipe(car1, y_car, race_slot1, race_slot_y)
    time.sleep(1)
    swipe(car2, y_car, race_slot2, race_slot_y)
    time.sleep(1)
    swipe(car3, y_car, race_slot3, race_slot_y)
    time.sleep(1)
    swipe(car4, y_car, race_slot4, race_slot_y)
    time.sleep(1)
    swipe(car5, y_car, race_slot5, race_slot_y)
    time.sleep(7)


def skip_ingame():
    print("skipping ingame")
    x, y = False, False
    check_accept = False
    times_checked = 0
    x3, x4, y3, y4 = resize_ranges(1000, 1200, 55, 95, resize_values)
    while not check_accept and times_checked < 5:
        x, y = random.randint(x3, x4), random.randint(y3, y4)
        tap(x, y)
        time.sleep(5)
        tap(x, y)
        check_accept = check_accept_skip()
        times_checked += 1
    x1, x2, y1, y2 = resize_ranges(1280, 1700, 780, 860, resize_values)
    skip_accept_coords = random.randint(x1, x2), random.randint(y1, y2)
    tap(skip_accept_coords[0], skip_accept_coords[1])
    time.sleep(5)
    if x == False or y == False:
        x, y = random.randint(x3, x4), random.randint(y3, y4)
    tap(x, y)
    time.sleep(2)
    tap(x + 10, y + 10)
    time.sleep(2)
    tap(x, y)
    time.sleep(2)


def check_accept_skip():
    print("checking accept skip")
    img_path = capture_screenshot()
    img = Image.open(img_path)
    x, y = resize_coordinates(1290, 830, resize_values)
    color = img.getpixel((x, y))
    remove_screenshot(img_path)
    if color == (26, 199, 213, 255):
        print(color)
        print("skip_accept found!")
        return True
    else:
        print('Not skipped yet found')
        return False


def get_upgrade_after_match():
    print("getting upgrade after match")
    upgrade_color = (0, 101, 239, 255)
    img_path = capture_screenshot()
    img = Image.open(img_path)
    x, y = resize_coordinates(1031, 178, resize_values)
    color = img.getpixel((x, y))
    print(color)
    remove_screenshot(img_path)
    if color == upgrade_color:
        time.sleep(1)
        x1, x2, y1, y2 = resize_ranges(860, 880, 1050, 1060, resize_values)
        rand_x, rand_y = random.randint(x1, x2), random.randint(y1, y2)
        tap(rand_x, rand_y)
        print("Upgrade found!")
        time.sleep(2)
        tap(rand_x, rand_y)


def count_prizecards():
    print("counting prizecards")
    star_color = (242, 165, 23, 255)
    img_path = capture_screenshot()
    img = Image.open(img_path)
    number_of_prizes = 0
    x, y = resize_coordinates(1910, 200, resize_values)
    color = img.getpixel((x, y))
    if color == star_color:
        number_of_prizes += 1
        x = resize_coordinate(2000, resize_values[0])
        color = img.getpixel((x, y))
        if color == star_color:
            number_of_prizes += 1
            x = resize_coordinate(2090, resize_values[0])
            color = img.getpixel((x, y))
            if color == star_color:
                number_of_prizes += 1
    else:
        number_of_prizes = 0
    print(number_of_prizes)
    return number_of_prizes, img, img_path


def collect_prizecards(img, number_of_prizes, img_path):
    print("collecting prizecards")
    prize_card_color = (239, 90, 36, 255)
    x_start, x_plus, y_start, y_plus = resize_ranges(195, 414, 413, 264, resize_values)
    for y in range(y_start, int(1000 * resize_values[1]), y_plus):
        for x in range(x_start, int(1900 * resize_values[0]), x_plus):
            color = img.getpixel((x, y))
            if color == prize_card_color:
                tap(x, y)
                time.sleep(2)
                tap(x, y)
                time.sleep(2)
                number_of_prizes -= 1
                if number_of_prizes == 0:
                    remove_screenshot(img_path)
                    return
    remove_screenshot(img_path)
    return


def tap_home():
    print("tapping home")
    x1, x2, y1, y2 = resize_ranges(940, 1030, 20, 115, resize_values)
    x, y = random.randint(x1, x2), random.randint(y1, y2)
    tap(x, y)
    time.sleep(2)


def full_event(stop_event):
    calculate_screen_size()
    event_number = 1
    while event_number <= 5:
        if stop_event.is_set():
            print("Stopping full event bot...")
            break
        ticket = True
        tap_home()
        tap_events()
        if not check_event_available(event_number):
            print("event not available")
            print("last event done")
            break
        tap_event(event_number)
        while ticket:
            screenshot = capture_screenshot()
            if check_ticket(screenshot):
                tap_play_event()
                tap_go_button_event()
                if check_cannot_play():
                    print("cannot play found")
                    event_number += 1
                    break
                tap_in_event_play()
                swipe_cars_to_slots()
                skip_ingame()
                get_upgrade_after_match()
                number_of_prizes, img, img_path = count_prizecards()
                collect_prizecards(img, number_of_prizes, img_path)
            else:
                if check_empty_ticket(screenshot):
                    print("empty Ticket found")
                    event_number += 1
                else:
                    print("no Ticket found")
                ticket = False
            remove_screenshot(screenshot)



def remove_screenshot(filename):
    os.remove(filename)


if __name__ == "__main__":
    # Run any code you want to execute when the script is run directly
    full_event()
