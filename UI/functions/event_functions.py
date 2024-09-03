from PIL import Image
import os
import random
from datetime import datetime
import time
import subprocess
from config import resize_values
from .general_functions import capture_screenshot, remove_screenshot, swipe, tap, color_almost_same
from UI.bot_manager.db_assign import get_corresponding_assignees
from .resize_functions import resize_coordinate, resize_coordinates, resize_ranges, resize_same_factor, \
    calculate_screen_size
from .general_game_functions import check_cannot_play
from image_reader.event.event_cropper_V3 import get_event_name
from database.methods.db_events import get_event_id_by_name, get_all_active_events


def check_ticket(img_path):
    ticket_color = (248, 171, 23, 255)
    empty_ticket_color = (146, 146, 146, 255)
    print("checking ticket")
    with Image.open(img_path) as img:
        x, y = resize_coordinates(890, 1150, resize_values)
        color = img.getpixel((x, y))
        if color == ticket_color:
            print("Ticket found!")
            ticket_str = "Ticket"
            return ticket_str
        elif color == empty_ticket_color:
            print("empty Ticket found!")
            ticket_str = "Empty Ticket"
            return ticket_str
        else:
            print('No ticket found')
            ticket_str = "N/A"
            return ticket_str


def check_empty_ticket(img_path):
    print("checking empty ticket")
    with Image.open(img_path) as img:
        empty_ticket_color = (146, 146, 146, 255)
        x, y = resize_coordinates(890, 1150, resize_values)

        color = img.getpixel((x, y))
        if color == empty_ticket_color:
            print("empty Ticket found!")
            return True
        else:
            print('No ticket found')
            return False


def tap_event(event_number: int = 1):
    print("tapping event")
    y1, y2 = resize_coordinate(400, resize_values[1]), resize_coordinate(800, resize_values[1])
    y = random.randint(y1, y2)
    if event_number == 1 or event_number == 3:
        x1, x2 = resize_coordinate(840, resize_values[0]), resize_coordinate(1180, resize_values[0])
        x = random.randint(x1, x2)
    elif event_number == 2 or event_number == 4:
        x1, x2 = resize_coordinate(1480, resize_values[0]), resize_coordinate(1890, resize_values[0])
        x = random.randint(x1, x2)
    elif event_number == 5:
        x1, x2 = resize_coordinate(2000, resize_values[0]), resize_coordinate(2150, resize_values[0])
        x = random.randint(x1, x2)
    else:
        x1, x2 = resize_coordinate(2000, resize_values[0]), resize_coordinate(2150, resize_values[0])
        x = random.randint(x1, x2)
    tap(x, y)
    time.sleep(2)


def check_event_available(event_number: int = 1):
    tap_home()
    tap_events()
    if event_number > 3:
        swipe_coords = resize_ranges(1320, 700, 330, 330, resize_values)
        for i in range(event_number - 3):
            swipe(swipe_coords[0], swipe_coords[2], swipe_coords[1], swipe_coords[3])
        x, y = resize_coordinates(2180, 266, resize_values)
    else:
        if event_number == 1:
            x, y = resize_coordinates(1080, 266, resize_values)
        if event_number == 2:
            x, y = resize_coordinates(1700, 266, resize_values)
        if event_number == 3:
            x, y = resize_coordinates(2180, 266, resize_values)

    unavailable_color = (112, 112, 112, 255)
    display_img_path = capture_screenshot()
    with Image.open(display_img_path) as img:
        color = img.getpixel((x, y))
        if color == unavailable_color:
            print("event not available")
            is_available = False
        else:
            print("event available")
            is_available = True

    return is_available, display_img_path


def swipe_left_one_event():
    x1_swipe, x2_swipe, y1, y2 = resize_ranges(1335, 700, 300, 400, resize_values)
    x_step = int((x1_swipe - x2_swipe)*0.25)

    swipe(x1_swipe-x_step, y1, x2_swipe, y1)  # Dont know how but this is perfect
    swipe(x1_swipe, y1, x1_swipe+5, y2) #stop the movements Y-Changes otherwise counts as a tap
    time.sleep(0.2)


def get_event_number_inactive(save_display=False):
    unavailable_x1, unavailable_y1 = resize_coordinates(1120, 290, resize_values)
    unavailable_color = (112, 112, 112, 255)
    event_number = 0
    open_events_img_paths = []
    event_unavailable = False

    tap_home()
    tap_events()
    while not event_unavailable:
        if event_number > 0:
            swipe_left_one_event()

        display_img_path = capture_screenshot()
        time.sleep(1)
        with Image.open(display_img_path) as img:
            color = img.getpixel((unavailable_x1, unavailable_y1))
            print(color)
            if color_almost_same(color, unavailable_color, tolerance=10):
                print("event not available")
                event_unavailable = True
            else:
                print("event available")
                event_unavailable = False
                open_events_img_paths.append(display_img_path)
        event_number += 1
        time.sleep(0.5)
    inactive_event_number = event_number
    tap_home()
    tap_events()
    if save_display:
        return inactive_event_number, open_events_img_paths,
    else:
        for img_path in open_events_img_paths:
            remove_screenshot(img_path)
        return inactive_event_number


def event_requirements_met(img_path):
    x, y = resize_coordinates(645, 288, resize_values)
    not_met_color = (67, 67, 67, 255)

    with Image.open(img_path) as img:
        color = img.getpixel((x, y))
        print(color)
        if color_almost_same(color, not_met_color, tolerance=5):
            print("event requirements not met")
            return False
        else:
            print("event requirements met")
            return True


def tap_play_event():
    print("tapping play event")
    x1, x2, y1, y2 = resize_ranges(1700, 1800, 1110, 1200, resize_values)
    rand_tap = (random.randint(x1, x2),
                random.randint(y1, y2))
    tap(rand_tap[0], rand_tap[1])
    time.sleep(2)


# def check_cannot_play():
#     print("checking cannot play")
#     cannot_play_color = (51, 51, 51, 255)
#     selected_hand_fault_color = (27, 31, 40, 255)
#     selected_hand_fault_coords = (490, 815)
#     img_path = capture_screenshot()
#     img = Image.open(img_path)
#     x, y = resize_coordinates(720, 750, resize_values)
#     color1 = img.getpixel((x, y))
#     x, y = resize_coordinates(selected_hand_fault_coords[0], selected_hand_fault_coords[1], resize_values)
#     color2 = img.getpixel((x, y))
#     remove_screenshot(img_path)
#     print(color1, color2)
#     if color1 == cannot_play_color or color2 == selected_hand_fault_color:
#         print("cannot play found!")
#         return True
#     else:
#         print('cannot play not found')
#         return False


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


def swipe_cars_to_slots(assignees):
    print("swiping cars to slots")
    y1, y2 = resize_same_factor(1110, 1150, resize_values[1])
    y_car = random.randint(y1, y2)
    car1 = random.randint(int(490 * resize_values[0]), int(520 * resize_values[0]))
    car2 = random.randint(int(880 * resize_values[0]), int(920 * resize_values[0]))
    car3 = random.randint(int(1280 * resize_values[0]), int(1300 * resize_values[0]))
    car4 = random.randint(int(1560 * resize_values[0]), int(1600 * resize_values[0]))
    car5 = random.randint(int(1900 * resize_values[0]), int(1930 * resize_values[0]))
    carlist = [car1, car2, car3, car4, car5]

    race_slot_y = random.randint(int(700 * resize_values[1]), int(800 * resize_values[1]))
    race_slot1 = random.randint(int(200 * resize_values[0]), int(300 * resize_values[0]))
    race_slot2 = random.randint(int(610 * resize_values[0]), int(700 * resize_values[0]))
    race_slot3 = random.randint(int(1050 * resize_values[0]), int(1150 * resize_values[0]))
    race_slot4 = random.randint(int(1460 * resize_values[0]), int(1570 * resize_values[0]))
    race_slot5 = random.randint(int(1880 * resize_values[0]), int(2000 * resize_values[0]))
    slot_list = [race_slot1, race_slot2, race_slot3, race_slot4, race_slot5]

    if assignees:
        for assignee in assignees:
            print(assignee)
            swipe(carlist[assignee[1] - 1], y_car, slot_list[assignee[0] - 1], race_slot_y)
            time.sleep(0.5)
    else:
        swipe(car1, y_car, race_slot1, race_slot_y)
        time.sleep(0.5)
        swipe(car2, y_car, race_slot2, race_slot_y)
        time.sleep(0.5)
        swipe(car3, y_car, race_slot3, race_slot_y)
        time.sleep(0.5)
        swipe(car4, y_car, race_slot4, race_slot_y)
        time.sleep(0.5)
        swipe(car5, y_car, race_slot5, race_slot_y)
        time.sleep(0.5)


def skip_ingame():
    print("skipping ingame")
    x, y = False, False
    check_accept = False
    times_checked = 0
    x3, x4, y3, y4 = resize_ranges(1000, 1200, 55, 95, resize_values)
    while not check_accept and times_checked < 5:
        x, y = random.randint(x3, x4), random.randint(y3, y4)
        time.sleep(2)
        tap(x, y)
        time.sleep(3)
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
    time.sleep(3)


def check_accept_skip():
    print("checking accept skip")
    img_path = capture_screenshot()
    with Image.open(img_path) as img:
        x, y = resize_coordinates(1290, 830, resize_values)
        refresh_color_color = (90, 197, 159, 255)
        refresh_x, refresh_y = resize_coordinates(2107, 44, resize_values)
        color = img.getpixel((x, y))
        refresh_color = img.getpixel((refresh_x, refresh_y))
        print(color)
        if color == (27, 199, 214, 255):
            print(color)
            print("skip_accept found!")
            returnbool = True
        elif refresh_color == refresh_color_color:
            print(color)
            print("refresh found!")
            print("swipe_cars failed!")
            swipe_cars_fault()
            returnbool = check_accept_skip()
        else:
            print('Not skipped yet found')
            returnbool = False
    remove_screenshot(img_path)
    return returnbool


def swipe_cars_fault():
    time.sleep(1)
    x1, x2, y1, y2 = resize_ranges(2100, 2120, 40, 45, resize_values)
    rand_x, rand_y = random.randint(x1, x2), random.randint(y1, y2)
    tap(rand_x, rand_y)
    time.sleep(1)
    swipe_cars_to_slots()
    time.sleep(3)


def get_upgrade_after_match():
    print("getting upgrade after match")
    upgrade_color = (0, 101, 239, 255)
    img_path = capture_screenshot()
    with Image.open(img_path) as img:
        x, y = resize_coordinates(1031, 178, resize_values)
        color = img.getpixel((x, y))
        print(color)
        if color == upgrade_color:
            time.sleep(1)
            x1, x2, y1, y2 = resize_ranges(860, 880, 1050, 1060, resize_values)
            rand_x, rand_y = random.randint(x1, x2), random.randint(y1, y2)
            tap(rand_x, rand_y)
            print("Upgrade found!")
            time.sleep(2)
            tap(rand_x, rand_y)
            return True, img_path
        else:
            print('Upgrade not found')
            return False, img_path


def count_prizecards(img_path=None):
    print("counting prizecards")
    star_color = (242, 165, 23, 255)
    if img_path is None:
        img_path = capture_screenshot()
    with Image.open(img_path) as img:
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
        return number_of_prizes, img_path


def collect_prizecards(number_of_prizes, img_path):
    print("collecting prizecards")

    if number_of_prizes == 0:
        remove_screenshot(img_path)
        return
    prize_card_color = (239, 90, 36, 255)
    x_start, x_plus, y_start, y_plus = resize_ranges(195, 415, 413, 264, resize_values)

    with Image.open(img_path) as img:
        for y in range(y_start, int(1000 * resize_values[1]), y_plus):
            for x in range(x_start, int(1900 * resize_values[0]), x_plus):
                color = img.getpixel((x, y))
                print(f'for {x}, {y}: color({color})')
                if color == prize_card_color:
                    tap(x, y)
                    time.sleep(1)
                    tap(x, y)
                    time.sleep(1)
                    number_of_prizes -= 1
                    if number_of_prizes == 0:
                        break
            if number_of_prizes == 0:
                break  # Breaks out of the outer loop

    remove_screenshot(img_path)


def tap_home():
    print("tapping home")
    x1, x2, y1, y2 = resize_ranges(940, 1030, 20, 115, resize_values)
    x, y = random.randint(x1, x2), random.randint(y1, y2)
    tap(x, y)
    time.sleep(2)


# def full_event(stop_event):
#     global resize_values
#     resize_values = calculate_screen_size()
#     print(resize_values)
#     event_number = 1
#     while event_number <= 5:
#         if stop_event.is_set():
#             print("Stopping full event bot...")
#             break
#         ticket = True
#         tap_home()
#         tap_events()
#         if not check_event_available(event_number):
#             print("event not available")
#             print("last event done")
#             break
#         tap_event(event_number)
#         while ticket:
#             screenshot = capture_screenshot()
#             if check_ticket(screenshot):
#                 tap_play_event()
#                 tap_go_button_event()
#                 if check_cannot_play():
#                     print("cannot play found")
#                     event_number += 1
#                     break
#                 tap_in_event_play()
#                 swipe_cars_to_slots()
#                 skip_ingame()
#                 get_upgrade_after_match()
#                 number_of_prizes, img, img_path = count_prizecards()
#                 collect_prizecards(img, number_of_prizes, img_path)
#             else:
#                 if check_empty_ticket(screenshot):
#                     print("empty Ticket found")
#                     event_number += 1
#                 else:
#                     print("no Ticket found")
#                 ticket = False
#             remove_screenshot(screenshot)



def full_event_V2():  # ADD STOP_event
    calculate_screen_size()
    len_active_events = len(get_all_active_events())
    for event_number in range(len_active_events):
        # Tap home
        tap_home()

        # Tap events
        tap_events()
        print(f'Event number: {event_number}')
        if event_number:
            print(f'Event number: {event_number}')
            for i in range(event_number):
                swipe_left_one_event()
        tap_event(1)
        ticket = True
        screenshot = capture_screenshot()
        event_name = get_event_name(screenshot)
        event_id = get_event_id_by_name(event_name)
        if not event_id:
            print('Retrying event_id')
            new_event_name = event_name[:-6]
            event_id = get_event_id_by_name(new_event_name)
        remove_screenshot(screenshot)

        # While ticket stay in this event
        while ticket:

            screenshot = capture_screenshot()
            ticket_str = check_ticket(screenshot)
            if event_requirements_met(screenshot):
                if ticket_str == "Ticket":
                    if not event_id:
                        event_name = get_event_name(screenshot)
                        event_id = get_event_id_by_name(event_name)
                        if not event_id:
                            print('Retrying event_id')
                            new_event_name = event_name[:-10]
                            event_id = get_event_id_by_name(new_event_name)
                    # Tap play
                    tap_play_event()



                    # Tap go button
                    tap_go_button_event()

                    if check_cannot_play():
                        print("cannot play found")
                        event_number += 1
                        remove_screenshot(screenshot)
                        break
                    racetypes_screenshot = capture_screenshot()
                    assignees = get_corresponding_assignees(event_id, racetypes_screenshot)
                    remove_screenshot(racetypes_screenshot)
                    tap_in_event_play()
                    swipe_cars_to_slots(assignees)

                    skip_ingame()
                    can_ad_upgrade, img_path = get_upgrade_after_match()
                    if can_ad_upgrade:
                        remove_screenshot(img_path)
                        number_of_prizes, img_path = count_prizecards()

                    else:
                        number_of_prizes, img_path = count_prizecards(img_path=img_path)

                    collect_prizecards(number_of_prizes, img_path)
                else:
                    if ticket_str == "Empty Ticket":
                        print("empty Ticket found")
                        event_number += 1
                    else:
                        print("no Ticket found")
                    ticket = False
            else:
                print("event requirements not met")
                event_number += 1
                ticket = False
            remove_screenshot(screenshot)


def swipe_right_event():
    x1, x2, y1, y2 = resize_ranges(1195, 657, 237, 237, resize_values)
    swipe(x1, y1, x2, y2)
