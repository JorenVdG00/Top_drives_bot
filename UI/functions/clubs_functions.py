from PIL import Image
from UI.functions.general_functions import tap, swipe, swipe_and_hold, capture_screenshot, remove_screenshot
from UI.functions.event_functions import swipe_cars_to_slots, skip_ingame, check_accept_skip, tap_in_event_play, tap_events, claim_event, check_event_ended, get_upgrade_after_match
from UI.functions.general_game_functions import tap_home, get_sort_toggle, tap_sort_asc, un_swipe_cars, tap_requirements_1, \
    tap_requirements_2, tap_requirements_tab, swipe_cars, get_missing_slots
from config import BOT_SCREENSHOTS_DIR, resize_values
from UI.functions.resize_functions import resize_coordinate, resize_coordinates, resize_ranges, resize_same_factor, \
    calculate_screen_size
from ImageTools.utils.image_utils import color_almost_matches, resize_image, screenshot_context
from ImageTools.utils.data_utils import find_differences
from ImageTools.Clubs.choose_club_event import get_club_pick_score
from ImageTools.Clubs.clean_clubs import weight_to_team
from ImageTools.Clubs.club_cropper import crop_club_info, get_club_event_names, get_club_name, crop_in_event_club_info
from ImageTools.Clubs.fix_problems import check_problem, get_car_with_repairs
from ImageTools.cropper.coords import club_coordinates
from scraper.active_club_scraper import refresh_club_info
from database.methods.db_events import get_req_id, get_track_set, get_club_from_name, get_req_list, get_played_matches, \
    play_club_event, get_club_track_set_of_name, get_req_num, end_active_club, get_active_club
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
    x1, x2, y1, y2 = resize_ranges(1400, 1450, 1000, 1050, resize_values)
    x, y = random.randint(x1, x2), random.randint(y1, y2)
    tap(x, y)
    time.sleep(1)


def check_club_rewards(img_path):
    x, y = resize_coordinates(1430, 1050, resize_values)
    club_reward_color = (25, 200, 212, 255)
    with Image.open(img_path) as img:

        color = img.getpixel((x, y))
        print(color)
        print(club_reward_color)
        if color_almost_matches(color, club_reward_color):
            return True
        else:
            return False


def tap_play_button_in_club():
    x, y = resize_coordinates(1350, 1150, resize_values)
    tap(x, y)


def check_play_button():
    from ImageTools.utils.image_utils import color_distance
    print('check_play_button')
    screenshot = capture_screenshot()
    is_playable = False
    x, y = 1350, 1144
    can_play_color = (41, 218, 220, 255)
    # rand_x, rand_y = (random.randint(*resize_ranges(1350, 1380, 1144, 1180, resize_values)[i:i + 2]) for i in (0, 2))
    with Image.open(screenshot) as img:
        resized_img = resize_image(img)
        color = resized_img.getpixel((x, y))
        print('play_color: ', str(can_play_color))
        print('can_play_color: ', str(color))
        print(color_distance(can_play_color, can_play_color))
        print(f'tol_20: {color_almost_matches(color, can_play_color, 20)}')
        print(f'tol_50: {color_almost_matches(color, can_play_color, 50)}')
        print(f'tol_70: {color_almost_matches(color, can_play_color, 70)}')
        if color_almost_matches(color, can_play_color, 20):
            # tap(rand_x, rand_y)
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
    print('go_button_good???')
    req_list = get_req_list(club_id)
    print(req_list)
    print('buttonstatus')
    button_status = is_blue_go_button()
    if button_status:
        print(f"{button_status}\n" * 20)
        if button_status == 'GO':
            x, y = resize_coordinates(1900, 1070, resize_values)
            tap(x, y)
            time.sleep(4)
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
    # fill the req_list with 0
    if not req1_num:
        for i in range(5):
            req_list.append([0])
    else:
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
    time.sleep(0.5)


def tap_play_club(event_dict):
    x1, x2, y1, y2 = resize_ranges(1800, 2000, 1180, 1220, resize_values)
    rand_x, rand_y = random.randint(x1, x2), random.randint(y1, y2)
    tap(rand_x, rand_y)
    time.sleep(1)
    can_play = check_play_button()
    print(can_play)
    time.sleep(0.5)
    if can_play:
        tap_play_button_in_club()
        time.sleep(0.5)
        # this_event = events[event_name]
        req1_id, req2_id = event_dict['req1_id'], event_dict['req2_id']
        req1_num, req2_num = get_req_num(req1_id), get_req_num(req2_id)
        req_list = generate_req_list(req1_num, req2_num)

        time.sleep(0.5)

        swipe_req_to_slot(req_list)
        time.sleep(0.5)
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
    print(req_list)
    un_swipe_cars()
    time.sleep(0.5)
    screenshot = capture_screenshot()
    sort_toggle = get_sort_toggle(screenshot)
    remove_screenshot(screenshot)

    time.sleep(0.5)
    if sort_toggle and (sort_toggle != 'ASC'):
        tap_sort_asc(sort_toggle)

    if count1 + count2 > 5:
        min_count = min(count1, count2)
        tap_requirements_tab()
        time.sleep(0.5)
        tap_requirements_1()
        time.sleep(0.5)
        tap_requirements_2()
        time.sleep(0.5)
        tap_requirements_tab()
        time.sleep(0.5)
        swipe_cars(1, min_count)
        tap_requirements_1()
        time.sleep(0.5)
        tap_requirements_2()
        time.sleep(0.5)
        swipe_cars(min_count + 1, 5)
        time.sleep(0.5)

    elif count1 + count2 == 0:
        swipe_cars(1, 5)

    else:
        tap_requirements_tab()
        time.sleep(0.5)
        if count2 != 0:
            tap_requirements_1()
            time.sleep(0.5)
        for j in range(5):
            if req_list[j] == 2:
                tap_requirements_tab()
                time.sleep(0.5)
                tap_requirements_2()
                time.sleep(0.5)
                tap_requirements_1()
                time.sleep(0.5)
            print(f'swiping_cars {j+1}')
            swipe_cars(j + 1, j + 1)


def fix_missing_slots(req_list, missing_slot, number=0):
    count1, count2 = count_reqs(req_list)
    fixed = False
    loop_number = number
    while not fixed:
        if len(req_list[missing_slot - 1]) == 2:
            tap_requirements_tab()
            time.sleep(0.5)
            tap_requirements_1()
            time.sleep(0.5)
            tap_requirements_2()
            time.sleep(0.5)
            swipe_cars(count1, count2, (count2 // 2 + count2 % 1) + loop_number)
            time.sleep(0.5)
        elif req_list[missing_slot - 1] == 1:
            tap_requirements_tab()
            time.sleep(0.5)
            tap_requirements_1()
            time.sleep(0.5)
            swipe_cars(count1, count2, (count1 // 2 + count1 % 1))
            time.sleep(0.5)
        else:
            tap_requirements_tab()
            time.sleep(0.5)
            tap_requirements_2()
            time.sleep(0.5)
            swipe_cars(count1, count2, (count2 // 2 + count2 % 1))
            time.sleep(0.5)
        missing_slots = get_missing_slots()
        if missing_slots in missing_slots:
            fixed = False
            loop_number += 1
            if loop_number == 5 + number:
                return False
        else:
            return True


def tap_play_event(event_index, event_name, events, nr_looped=0):
    screenshot_list = []



    # Capture screenshots as you swipe
    for _ in range((event_index) // 3):  # Adding 2 to number ensures proper division and rounding up
        screenshot_list.append(capture_screenshot())
        swipe_clubs_3_up()

    # Gather all club names from the screenshots
    names = [club_name for screenshot in screenshot_list for club_name in get_club_event_names(screenshot)]

    try:
        index = names.index(event_name)
        click_event(index)
        time.sleep(0.5)
        can_play = tap_play_club(events)
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
            time.sleep(0.5)

            can_play = tap_play_club(events)
            time.sleep(0.5)
            if can_play:
                return can_play
        tap_play_event(event_index + 3, event_name, events, nr_looped)

    finally:
        for screen in screenshot_list:
            remove_screenshot(screen)


def click_event(number):
    check_number = number % 3
    print('checknnubmer: ', check_number)
    x1, x2 = resize_same_factor(1600, 2000, resize_values[0])
    rand_x = random.randint(x1, x2)
    y1, y2 = resize_same_factor(club_coordinates['club_events']['club_event_y'][f'club_event_y{check_number + 1}'][0],
                                club_coordinates['club_events']['club_event_y'][f'club_event_y{check_number + 1}'][1],
                                resize_values[1])
    rand_y = random.randint(y1, y2)
    print('tapping :', (rand_x, rand_y))
    # swipe(rand_x, rand_y, rand_x, rand_y, 50)
    tap(rand_x, rand_y)
    time.sleep(2)


def tap_back():
    x1, x2, y1, y2 = resize_ranges(1600, 1650, 170, 210, resize_values)
    randx, randy = random.randint(x1, x2), random.randint(y1, y2)
    tap(randx, randy)
    time.sleep(1)


def choose_club_event():
    new_events = True
    events_checked = 0
    checked_names = []
    number_lost_events = 0
    last_clicked_club_event = None
    events = {}

    while new_events:
        screenshot = capture_screenshot()
        if check_club_rewards(screenshot):
            time.sleep(0.5)
            claim_club_reward()
            remove_screenshot(screenshot)
            screenshot = None


        # --GET CLUB NAMES
        club_names = []
        screenshot = capture_screenshot() if screenshot is None else screenshot
        names = get_club_event_names(screenshot)
        remove_screenshot(screenshot)

        for club_name in names:
            club_names.append(club_name)

        for i in range((events_checked+1) // 3):
            swipe_clubs_3_up()
            time.sleep(0.5)

            screenshot = capture_screenshot()
            names = get_club_event_names(screenshot)
            remove_screenshot(screenshot)

            for name in names:
                club_names.append(name)


        #TODO: CHECK NAMES VS PREV POS
        lost_events, added_events = find_differences(checked_names, club_names)
        events_checked -= len(lost_events)
        number_lost_events += len(lost_events)


        #TODO add stop
        # if len(checked_names)+3 <= events_checked:
        #     new_events = False
        #
        # if not added_events:
        #     events_checked += 3




        added_index_dict = {}
        for added_event in added_events:
            addex_index = club_names.index(added_event)
            added_index_dict[added_event] = addex_index

        with screenshot_context() as screenshot:
            if has_joined_event(screenshot):
                tap_back()
            else:
                click_event(2)
                time.sleep(0.5)
                tap_back()

        for event, index in added_index_dict.items():
            for i in range(index // 3):
                swipe_clubs_3_up()
                time.sleep(0.5)

            screenshot = capture_screenshot()
            names = get_club_event_names(screenshot)
            remove_screenshot(screenshot)

            if event in names:
                click_event(names.index(event))
                time.sleep(0.5)

                screenshot = capture_screenshot()
                print('checking hasJoined: ', has_joined_event(screenshot))
                while not has_joined_event(screenshot):
                    print('reclicking event bcs not hasjoined')
                    remove_screenshot(screenshot)
                    click_event(names.index(event))
                    screenshot = capture_screenshot()
                remove_screenshot(screenshot)


                screenshot = capture_screenshot()
                club_dir = crop_club_info(screenshot, temp_club_dir)
                img_path = os.path.join(club_dir, 'weight.png')
                valid_event = weight_to_team(img_path)
                if not valid_event:
                    with screenshot_context() as screenshot:
                        if has_joined_event(screenshot):
                            tap_back()
                    continue
                club_pick_score, fixed_data = get_club_pick_score(club_dir)
                print('club_pick_score', club_pick_score)

                if club_pick_score is None:
                    checked_names.append(event)
                    with screenshot_context() as screenshot:
                        if has_joined_event(screenshot):
                            tap_back()
                    continue


                req1_id = get_req_id(fixed_data['reqs1']['name'])
                if fixed_data['reqs2']:
                    req2_id = get_req_id(fixed_data['reqs2']['name'])
                else:
                    req2_id = None
                club_set_id = get_track_set(fixed_data['event_type'])

                events[event] = {'name': event, 'pick_score': club_pick_score, 'rq': fixed_data['rq'],
                                      'club_set_id': club_set_id, 'req1_id': req1_id, 'req2_id': req2_id}

                if events[event]['pick_score'] < 2500:
                    print('Playong club under 50 pickscore')
                    can_play = tap_play_club(events[event])
                    if can_play:
                        club_id = add_club_event(event, fixed_data['rq'], club_set_id, req1_id, req2_id)
                        return club_id
                    else:
                        checked_names.append(event)
                        events_checked += 1
                        tap_back()
                        continue
                else:
                    #ADD TO POOL
                    events.pop(event)
                    checked_names.append(event)
                    events_checked += 1
                    tap_back()
                    continue


            else:
                with screenshot_context() as screenshot:
                    if has_joined_event(screenshot):
                        tap_back()
                continue
        #
        # # # #TODO: CHECK POSITIONS
        # # # for club_name in club_names:
        # # #
        # # # for lost_event in lost_events:
        # # #     index = checked_names.index(lost_event)
        # #
        # # #TODO: CHANGE CHECKED NAMES
        # # for lost_event in lost_events:
        # #     checked_names.remove(lost_event)
        # # for added_event in added_events:
        # #     checked_names.append(added_event)
        # # for i in range(len(lost_events)):
        # #     events_checked -= 1
        # #
        # # # TODO: TOO COMPLICATED WILL CHECK 1 BY 1 (WAIT)!!!!!!!!!!!
        # #
        # # # club_names = []
        # # # screenshot = capture_screenshot()
        # # # names = get_club_event_names(screenshot)
        # # # remove_screenshot(screenshot)
        # # #
        # # # for name in names:
        # # #     club_names.append(name)
        # # #
        # # # for i in range(events_checked // 3):
        # # #     swipe_clubs_3_up()
        # # #     time.sleep(0.5)
        #
        # # for i in range(events_checked // 3):
        # #     swipe_clubs_3_up()
        # #     time.sleep(0.5)
        # #
        # # if events_checked % 3 == 0:
        # #     screenshot = capture_screenshot()
        # #     names = get_club_event_names(screenshot)
        # #     remove_screenshot(screenshot)
        # #
        # #     for name in names:
        # #         already_checked = 0
        # #         if name not in checked_names:
        # #             checked_names.append(name)
        # #         if name in checked_names:
        # #             new_events = False
        # #             break
        #
        # click_event(events_checked)
        # time.sleep(0.5)
        # screenshot = capture_screenshot()
        #
        # print('checking hasJoined: ', has_joined_event(screenshot))
        # while not has_joined_event(screenshot):
        #     print('reclicking event bcs not hasjoined')
        #     remove_screenshot(screenshot)
        #     click_event(events_checked)
        #     screenshot = capture_screenshot()
        # remove_screenshot(screenshot)
        # screenshot = capture_screenshot()
        # club_dir = crop_club_info(screenshot, temp_club_dir)
        # img_path = os.path.join(club_dir, 'weight.png')
        # valid_event = weight_to_team(img_path)
        # if not valid_event:
        #     continue
        # club_pick_score, fixed_data = get_club_pick_score(club_dir)
        # print('club_pick_score', club_pick_score)
        #
        # if club_pick_score is None:
        #     events_checked += 1
        #     continue
        #
        # req1_id = get_req_id(fixed_data['reqs1']['name'])
        # if fixed_data['reqs2']:
        #     req2_id = get_req_id(fixed_data['reqs2']['name'])
        # else:
        #     req2_id = None
        # club_set_id = get_track_set(fixed_data['event_type'])
        #
        # event_name = fixed_data['name']
        # events[event_name] = {'name': event_name, 'pick_score': club_pick_score, 'rq': fixed_data['rq'],
        #                       'club_set_id': club_set_id, 'req1_id': req1_id, 'req2_id': req2_id,
        #                       'number': events_checked}
        #
        # if events[event_name]['pick_score'] < 50:
        #     print('Playong club under 50 pickscore')
        #     can_play = tap_play_club(events)
        #     if can_play:
        #         club_id = add_club_event(event_name, fixed_data['rq'], club_set_id, req1_id, req2_id)
        #         return club_id
        # tap_back()
        # events_checked += 1

        # print('tapBACK')
        # time.sleep(3)
        # print('tapHOME')
        # tap_home()
        # tap_events()
        # tap_clubs()

    can_play = False
    while not can_play:
        sorted_events = sorted(events, key=lambda x: events[x]['pick_score'])
        event_name = sorted_events[0]

        try_event_dict = events[event_name]

        club_event_index = get_club_event_index(event_name, events_checked)
        if club_event_index is None:
            continue

        click_event(club_event_index)
        can_play = tap_play_club(try_event_dict)

        if can_play:
            req1_id = get_req_id(try_event_dict['reqs1']['name'])
            req2_id = get_req_id(try_event_dict['reqs2']['name'])
            club_set_id = get_track_set(try_event_dict['event_type'])
            club_id = add_club_event(event_name, try_event_dict['rq'], club_set_id, req1_id, req2_id)
            return club_id
        else:
            sorted_events.pop(0)

def get_club_event_index(event_name, events_checked):
    club_names = []
    screenshot = capture_screenshot()
    names = get_club_event_names(screenshot)
    remove_screenshot(screenshot)

    for club_name in names:
        club_names.append(club_name)
        if event_name in club_name:
            return club_names.index(event_name)
    for i in range(events_checked // 3):
        swipe_clubs_3_up()
        time.sleep(0.5)

        screenshot = capture_screenshot()
        names = get_club_event_names(screenshot)
        remove_screenshot(screenshot)

        for name in names:
            club_names.append(name)
            if name == event_name:
                return club_names.index(event_name)
    return None

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
        if  color_almost_matches(color, gray_go_color, 10):
            status = 'MISSING'
        elif color_almost_matches(color, red_go_color, 10):
            status = 'EXCEEDING'
        elif color_almost_matches(color, blue_go_color, 10):
            status = 'GO'
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

    # ALREADY IN AN EVENT
    has_joined = has_joined_event(screenshot)
    print(f'has_joined: {has_joined}')
    if has_joined:
        play_current_active()
        time.sleep(2)
        active_club_id = get_active_club()
        print(f'club_id: {club_id}')
        if not club_id:
            screenshot = capture_screenshot()
            club_info = crop_in_event_club_info(screenshot)
            print(f'club_info: {club_info}')
            club_id = get_club_from_name(club_info['event_name'])
        # if club_id != active_club_id:
            end_active_club()
            print(f'club_id: {club_id}')
            track_set_id = get_club_track_set_of_name(club_info['event_type'])
            print(f'track_set_id: {track_set_id}')
            if club_info['req1_id']:
                req1_id = club_info['req1_id']
            else:
                req1_id = None

            if club_info['req2_id']:
                req2_id = club_info['req2_id']
            else:
                req2_id = None

            if club_info:
                club_id = add_club_event(club_info['event_name'], club_info['rq'], track_set_id, req1_id,
                                         req2_id)
        go_button_good(club_id)
    else:
        # CHOOSE AN EVENT
        club_id = choose_club_event()
    remove_screenshot(screenshot)
    club_ended = False
    played_matches = get_played_matches(club_id)
    print(played_matches)
    while not club_ended:
        can_play = check_play_button()
        if can_play:
            tap_play_button_in_club()
            time.sleep(0.5)
            go_button_good(club_id)
            time.sleep(0.5)
            tap_in_event_play()
            time.sleep(3)
            swipe_cars_to_slots()
            time.sleep(0.5)
            play_club_event(club_id)
            time.sleep(3)
            skip_ingame()
            check_accept_skip()
            get_upgrade_after_match()
            screenshot = capture_screenshot()
            if check_club_rewards(screenshot):
                end_active_club()
                club_ended = True
            remove_screenshot(screenshot)
        else: club_ended = check_club_rewards(club_id)



def check_play_in_event():
    play_color = (28, 200, 215,255)
    x,y = 850, 870
    is_play = False

    screenshot = capture_screenshot()
    with Image.open(screenshot) as img:
        resized_img = resize_image(img)
        color = resized_img.getpixel((x, y))
        if color_almost_matches(color, play_color, 10):
            is_play = True
        else:
            is_play = False
    remove_screenshot(screenshot)
    return is_play


if __name__ == '__main__':
    calculate_screen_size()
    req_list = generate_req_list(5, 2)
    swipe_req_to_slot(req_list)