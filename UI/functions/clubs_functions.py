from PIL import Image
from .general_functions import tap, swipe, swipe_and_hold, capture_screenshot, remove_screenshot
from .event_functions import swipe_cars_to_slots,skip_ingame, check_accept_skip, tap_in_event_play, tap_events
from .general_game_functions import tap_home, get_sort_toggle, tap_sort_asc, un_swipe_cars, tap_requirements_1, \
    tap_requirements_2, tap_requirements_tab, swipe_cars, get_missing_slots
from config import BOT_SCREENSHOTS_DIR, resize_values
from .resize_functions import resize_coordinate, resize_coordinates, resize_ranges, resize_same_factor, \
    calculate_screen_size
from ImageTools.utils.image_utils import color_almost_matches, resize_image
from ImageTools.Clubs.choose_club_event import get_club_pick_score
from ImageTools.Clubs.club_cropper import crop_club_info, get_club_event_names, get_club_name
from ImageTools.Clubs.fix_problems import check_problem, get_car_with_repairs
from ImageTools.cropper.coords import club_coordinates
from scraper.active_club_scraper import refresh_club_info
from database.methods.db_events import get_req_id, get_track_set, get_club_from_name, get_req_list, get_played_matches, play_club_event
from database.methods.db_adder import add_club_event
import os
import threading
import time
import random

temp_club_dir = os.path.join(BOT_SCREENSHOTS_DIR, 'clubs')


def tap_clubs():
    x1, x2, y1, y2 = resize_ranges(260, 520, 500, 750, resize_values)
    x, y = random.randint(x1, x2), random.randint(y1, y2)
    tap(x, y)
    time.sleep(1)


def claim_club_reward():
    x1, x2, y1, y2 = resize_ranges(1000, 770, 1050, 780, resize_values)
    x, y = random.randint(x1, x2), random.randint(y1, y2)
    tap(x, y)
    time.sleep(1)


def check_club_rewards(img_path):
    x, y = resize_coordinates(1030, 770, resize_values)
    club_reward_color = (25, 200, 212, 255)
    with Image.open(img_path) as img:
        color = img.getpixel((x, y))
        if color_almost_matches(color, club_reward_color):
            return True
        else:
            return False

def tap_play_button_in_club():
    x,y = resize_coordinates(1350, 1150, resize_values)
    tap(x,y)

def check_play_button():
    screenshot = capture_screenshot()
    is_playable = False
    x, y = 1350, 1144
    can_play_color = (41, 218, 220, 255)
    rand_x, rand_y = (random.randint(*resize_ranges(1350, 1380, 1144, 1180, resize_values)[i:i + 2]) for i in (0, 2))
    with Image.open(screenshot) as img:
        resized_img = resize_image(img)
        color = resized_img.getpixel((x, y))
        if color_almost_matches(color, can_play_color):
            tap(rand_x, rand_y)
            is_playable = True
        else:
            is_playable = False
    remove_screenshot(screenshot)
    return is_playable

def has_joined_event(img_path):
    x, y = resize_coordinates(1700, 1160, resize_values)
    play_event_color = (255, 196, 79, 255)

    with Image.open(img_path) as img:
        color = img.getpixel((x, y))
        if color_almost_matches(color, play_event_color):
            return True
        else:
            return False

def can_start_club_event(req_list):
    button_status = is_blue_go_button()
    if button_status == 'EXCEEDING':
        return False
    while True:
        button_status = is_blue_go_button()
        if button_status:
            if button_status == 'GO':
                x, y = resize_coordinates(1900, 1070, resize_values)
                tap(x, y)
                time.sleep(0.5)
                problem = check_problem()
                if problem in 'NO_PROBLEM':
                    tap_in_event_play()
                    swipe_cars_to_slots()
                    time.sleep(3)
                    skip_ingame()
                    check_accept_skip()
                    return True
                elif problem == 'CARS_REPAIR':
                    car_repairs = get_car_with_repairs()
                    for slot in car_repairs:
                        un_swipe_cars(slot)
                elif problem == 'EVENT_ENDED':
                    print('Event ended')
                    tap(x, y)
                    return False
                else:
                    return False
            elif button_status == 'MISSING':
                missing_slots = get_missing_slots()
                for missing_slot in missing_slots:
                    if fix_missing_slots(req_list, missing_slot):
                        continue
                    else:
                        return False


def go_button_good(club_id):
    req_list = get_req_list(club_id)
    button_status = is_blue_go_button()
    if button_status:
        if button_status == 'GO':
            x, y = resize_coordinates(1900, 1070, resize_values)
            tap(x, y)
            time.sleep(0.5)
            problem = check_problem()
            if problem in 'NO_PROBLEM':
                # time.sleep(5)
                # swipe_cars_to_slots()
                # skip_ingame()
                # check_accept_skip()
                # time.sleep(5)
                # tap(x,y)
                return True
            elif problem == 'CARS_REPAIR':
                car_repairs = get_car_with_repairs()
                for slot in car_repairs:
                    un_swipe_cars(slot)
            elif problem == 'EVENT_ENDED':
                print('Event ended')
                tap(x, y)
                return False
            else:
                return False
        elif button_status == 'MISSING':
            missing_slots = get_missing_slots()
            for missing_slot in missing_slots:
                if fix_missing_slots(req_list, missing_slot):
                    continue
                else:
                    return False
        elif button_status == 'EXCEEDING':
            swipe_req_to_slot(req_list)

def swipe_clubs_3_up():
    x1, x2, y1, y2 = resize_ranges(1600, 1600, 1160, 670, resize_values)
    swipe_and_hold(x1, y1, x2, y2, 3000, False)
    time.sleep(0.2)


def generate_req_list(req1_num, req2_num):
    req_list = []

    # Fill the req_list with req1 requirements
    for _ in range(req1_num):
        req_list.append([1])

    # Merge or add req2 requirements
    if req2_num:
        if req1_num == 5:
            # Merge req2 into req1
            for i in range(min(req1_num, req2_num)):
                req_list[i].append(2)
            # If req2_num exceeds req1_num, append additional lists for remaining req2
            for i in range(req1_num, req1_num + (req2_num - req1_num)):
                req_list.append([2])
        else:
            # Add req2 as new lists
            for _ in range(req2_num):
                req_list.append([2])

    return req_list

def play_current_active():
    x1, x2, y1, y2 = resize_ranges(1800, 2000, 1180, 1220, resize_values)
    rand_x, rand_y = random.randint(x1, x2), random.randint(y1, y2)
    tap(rand_x, rand_y)



def tap_play_club(event_name, events):
    x1, x2, y1, y2 = resize_ranges(1800, 2000, 1180, 1220, resize_values)
    rand_x, rand_y = random.randint(x1, x2), random.randint(y1, y2)
    tap(rand_x, rand_y)
    can_play = check_play_button()
    if can_play:
        tap_play_button_in_club()
        this_event = events[event_name]
        req1, req2 = events['reqs1'], events['reqs2']
        req1_num, req2_num = req1['number'], req2['number']
        req_list = generate_req_list(req1_num, req2_num)
        # this_event = events[event_name]
        # if this_event['reqs1'] and this_event['reqs2']:
        #     reqs_number = 2
        #     req_list = [this_event['reqs1']['number'], this_event['reqs2']['number']]
        #     print(this_event['reqs1'], this_event['reqs2'], reqs_number)
        # elif this_event['reqs1']:
        #     reqs_number = 1
        #     print(this_event['reqs1'], this_event['reqs2'], reqs_number)
        #     req_list = [this_event['reqs1']['number']]
        # else:
        #     reqs_number = 0
        #     print(this_event['reqs1'], this_event['reqs2'], reqs_number)
        #     req_list = None

        swipe_req_to_slot(req_list)
        club_started = can_start_club_event(req_list)
        return club_started
    else:
        return False

def count_reqs(req_list):
    count1 = sum(j == 1 for sublist in req_list for j in sublist)
    count2 = sum(j == 2 for sublist in req_list for j in sublist)
    return count1, count2

def swipe_req_to_slot(req_list):
    count1, count2 = count_reqs(req_list)
    un_swipe_cars()
    screenshot = capture_screenshot()
    remove_screenshot(screenshot)
    sort_toggle = get_sort_toggle(screenshot)

    if sort_toggle:
        tap_sort_asc(sort_toggle)

    if count1 + count2 > 5:
        min_count = min(count1, count2)
        tap_requirements_tab()
        tap_requirements_1()
        tap_requirements_2()
        swipe_cars(1, min_count)
        tap_requirements_1()
        tap_requirements_2()
        swipe_cars(min_count+1, 5)

    elif count1 + count2 == 0:
        swipe_cars(1, 5)

    else:
        tap_requirements_tab()
        tap_requirements_1()
        for j in range(5):
            if req_list.index(j)==2:
                tap_requirements_tab()
                tap_requirements_2()
                tap_requirements_1()
            swipe_cars(j+1, j+1)


def fix_missing_slots(req_list, missing_slot, number=0):
    count1, count2 = count_reqs(req_list)
    fixed = False
    loop_number = number
    while not fixed:
        if len(req_list[missing_slot-1]) == 2:
            tap_requirements_tab()
            tap_requirements_1()
            tap_requirements_2()
            swipe_cars(count1, count2, (count2//2+count2%1)+loop_number)
        elif req_list[missing_slot-1] == 1:
            tap_requirements_tab()
            tap_requirements_1()
            swipe_cars(count1, count2, (count1//2+count1%1))
        else:
            tap_requirements_tab()
            tap_requirements_2()
            swipe_cars(count1, count2, (count2//2+count2%1))


        missing_slots = get_missing_slots()
        if missing_slots in missing_slots:
            fixed = False
            loop_number += 1
            if loop_number == 5+number:
                return False
        else:
            return True








def tap_play_event(number, event_name, events, nr_looped=0):
    screenshot_list = []

    # Capture screenshots as you swipe
    for _ in range((number + 2) // 3):  # Adding 2 to number ensures proper division and rounding up
        screenshot_list.append(capture_screenshot())
        swipe_clubs_3_up()

    # Gather all club names from the screenshots
    names = [club_name for screenshot in screenshot_list for club_name in get_club_event_names(screenshot)]

    try:
        index = names.index(event_name)
        click_event(index)
        can_play = tap_play_club(event_name, events)
        return can_play

    except ValueError:
        nr_looped += 1
        if nr_looped > 4:
            number = events[1]['number']
            event_name = events[1]['name']
            nr_looped = 0
            events.pop(0)

        if event_name in names:
            index = names.index(event_name)
            click_event(index)
            can_play = (event_name, events)
            if can_play:
                return can_play
        tap_play_event(number + 3, event_name, events, nr_looped)

    finally:
        for screen in screenshot_list:
            remove_screenshot(screen)


def click_event(number):
    check_number = number % 3
    x1, x2 = resize_same_factor(1580, 2140, resize_values[0])
    rand_x = random.randint(x1, x2)
    y1, y2 = resize_same_factor(club_coordinates[f'club_event_y{check_number + 1}'][0],
                                club_coordinates[f'club_event_y{check_number + 1}'][1], resize_values[1])
    rand_y = random.randint(y1, y2)
    tap(rand_x, rand_y)


def tap_back():
    x1, x2, y1, y2 = resize_ranges(1600, 1650, 170, 210, resize_values)
    randx, randy = random.randint(x1, x2), random.randint(y1, y2)
    tap(randx, randy)


def choose_club_event():
    new_events = True
    events_checked = 0
    events = {}
    while new_events:
        for i in range(events_checked // 3):
            swipe_clubs_3_up()
        screenshot = capture_screenshot()
        names = get_club_event_names(screenshot)
        remove_screenshot(screenshot)
        checked_events = 0
        for name in names:
            if name in events:
                checked_events += 1
        if checked_events == 3:
            new_events = False
            break

        click_event(events_checked)
        screenshot = capture_screenshot()
        club_dir = crop_club_info(screenshot, temp_club_dir)
        club_pick_score, fixed_data = get_club_pick_score(club_dir)
        req1_id = get_req_id(fixed_data['reqs1']['name'])
        req2_id = get_req_id(fixed_data['reqs2']['name'])
        club_set_id = get_track_set(fixed_data['event_type'])

        event_name = fixed_data['name']
        events[event_name] = {'name': event_name, 'pick_score': club_pick_score, 'rq': fixed_data['rq'],
                              'club_set_id': club_set_id, 'req1_id': req1_id, 'req2_id': req2_id,
                              'number': events_checked}

        if club_pick_score == 1:
            can_play = tap_play_club(event_name, events)
            if can_play:
                club_id = add_club_event(event_name, fixed_data['rq'], club_set_id, req1_id, req2_id)
                return club_id
        tap_back()
        print('tapBACK')
        time.sleep(3)
        print('tapHOME')
        tap_home()
        tap_clubs()

    can_play = False
    while not can_play:
        sorted_events = sorted(events, key=lambda x: events[x]['pick_score'])
        try_event = sorted_events[0]
        number = try_event['number']
        event_name = try_event['name']
        can_play = tap_play_event(number, event_name, sorted_events)
        if can_play:
            req1_id = get_req_id(try_event['reqs1']['name'])
            req2_id = get_req_id(try_event['reqs2']['name'])
            club_set_id = get_track_set(try_event['event_type'])
            club_id = add_club_event(number, event_name, club_set_id, req1_id, req2_id)
            return club_id
        else:
            sorted_events.pop(0)


def is_blue_go_button():
    status = None
    x, y = 1900, 1070
    gray_go_color = (71, 90, 113, 255)
    blue_go_color = (36, 207, 216, 255)
    red_go_color = (216, 40, 45, 255)
    screenshot = capture_screenshot()
    with Image.open(screenshot) as img:
        resized_img = resize_image(img)
        color = resized_img.getpixel((x, y))
        if color == gray_go_color:
            status= 'MISSING'
        elif color == red_go_color:
            status ='EXCEEDING'
        elif color == blue_go_color:
            status ='GO'
    remove_screenshot(screenshot)
    return status



def full_clubs():
    refresh_club_info()

    tap_home()
    tap_events()
    tap_clubs()

    time.sleep(5)

    screenshot = capture_screenshot()
    if check_club_rewards(screenshot):
        claim_club_reward()
    remove_screenshot(screenshot)
    club_id = None
    screenshot = capture_screenshot()
    has_joined = has_joined_event(screenshot)
    if has_joined:
        club_name = get_club_name(screenshot)
        club_id = get_club_from_name(club_name)
        play_current_active()
        req_list = get_req_list(club_id)
        go_button_good(req_list)
    else:
        club_id = choose_club_event()
    remove_screenshot(screenshot)
    club_ended = False
    played_matches = get_played_matches(club_id)
    while club_ended or played_matches > 30:
        tap_play_button_in_club()
        go_button_good(club_id)
        tap_in_event_play()
        swipe_cars_to_slots()
        play_club_event(club_id)
        time.sleep(3)
        skip_ingame()
        check_accept_skip()
        screenshot = capture_screenshot()
        check_club_rewards(screenshot)
        remove_screenshot(screenshot)






