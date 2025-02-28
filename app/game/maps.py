# Initialize the check maps

# * Base check map
base_check_map = {
    "blue_go": "blue_go",
    "red_go": "red_go",
    "gray_go": "gray_go",
    "after_go_unavailable": "after_go_unavailable",
    "play_after_go": "play_after_go",
    "accept_skip": "accept_skip",
    "refresh": "refresh",
    "upgrade_after_match": "upgrade_after_match",
    "sort_asc": "sort_asc",
    "sort_desc": "sort_desc",
    "add_to_hand": "add_to_hand",
    "remove_from_hand": "remove_from_hand",
    "missing_slots_start": "missing_slots_start",
    "missing_slots_step": "missing_slots_step",
    "claim_event": "claim_event",
    "double_check": "double_check",
    "is_fusing": "is_fusing",
    "is_servicing": "is_servicing",
    "reset_hand": "reset_hand",
    "empty_garage_slot": "empty_garage_slot",
    "go_to_club": "go_to_club",
    "repair_slots_start": "repair_slots_start",
    "repair_slots_step": "repair_slots_step",
    "problem": "problem",
    "empty_garage_slot_step": "empty_garage_slot_step",
}

# * Club check map
club_check_map = {
    'club_rewards': 'club_rewards',
    'play_in_club': 'play_in_club',
    'play_club': 'play_club',
    'info_icon': 'info_icon',
    'exit_info': 'exit_info',
    'last_club': 'last_club',
    'right_score_half': 'right_score_half',
    'left_score_half': 'left_score_half',
}

# * Event check map
event_check_map = {
    'event_1': 'event_1',
    'event_2': 'event_2',
    'event_3': 'event_3',
    'available_event_1': 'available_event_1',
    'available_event_2': 'available_event_2',
    'available_event_3': 'available_event_3',
    'unavailable_event': 'unavailable_event',
    'unavailable_last_visible': 'unavailable_last_visible',
    'no_last_visible': 'no_last_visible',
    'event_reqs_not_met': 'event_reqs_not_met',
    'prize_star_1': 'prize_star_1',
    'prize_star_2': 'prize_star_2',
    'prize_star_3': 'prize_star_3',
    'prize_card_start': 'prize_card_start',
    'prize_card_step': 'prize_card_step',
    'ticket': 'ticket',
    'empty_ticket': 'empty_ticket',
}

#! #####################
# Initialize the action maps

# * Base action map
base_action_map = {
    'home': 'home',
    'events': 'events',
    'go': 'go_button',
    'play_after_go': 'play_after_go',
    'skip': 'skip',
    'skip_accept': 'skip_accept',
    'upgrade_after_match': 'upgrade_after_match',
    'claim_event': 'claim_event',
    'sort': 'sort_button',
    'sort_rq': 'sort_rq',
    'req_tab': 'requirements_tab',
    'req_1': 'requirements_1',
    'req_2': 'requirements_2',
    'unswipe_slots': 'unswipe_slots',
    'unswipe_step': 'unswipe_to_car',
    'garage_1_1': 'garage_1_1',
    'garage_2_1': 'garage_2_1',
    'garage_3_1': 'garage_3_1',
    'garage_1_2': 'garage_1_2',
    'garage_2_2': 'garage_2_2',
    'garage_3_2': 'garage_3_2',
    'ingame_car1': 'ingame_car1',
    'ingame_car2': 'ingame_car2',
    'ingame_car3': 'ingame_car3',
    'ingame_car4': 'ingame_car4',
    'ingame_car5': 'ingame_car5',
    'ingame_slot1': 'ingame_slot1',
    'ingame_slot2': 'ingame_slot2',
    'ingame_slot3': 'ingame_slot3',
    'ingame_slot4': 'ingame_slot4',
    'ingame_slot5': 'ingame_slot5',
    'reset_hand': 'reset_hand',
    'add_to_hand': 'add_to_hand',
    'exit_car': 'exit_car',
    'close_problem_go': 'close_problem_go',
    'hand_1': 'hand_1',
    'hand_2': 'hand_2',
    'hand_3': 'hand_3',
    'hand_4': 'hand_4',
    'hand_5': 'hand_5',
    'sort_button': 'sort_button',
    'unswipe_to_car': 'unswipe_to_car',
    'swipe_left_cars': 'swipe_left_cars',
    'back': 'back',
    'go_button': 'go_button',
    'requirements_tab': 'requirements_tab',
    'requirements_2': 'requirements_2',
    'requirements_1': 'requirements_1',
    'claim_prizes': 'claim_prizes',
    'close_problem_go': 'close_problem_go',
    'all_cars': 'all_cars',
}

# * Club action map	
club_action_map = {
        "clubs": "clubs",
        "claim_clubs": "claim_clubs",
        "play_in_club": "play_in_club",
        "play_club": "play_club",
        "club_event_1": "club_event_1",
        "club_event_2": "club_event_2",
        "club_event_3": "club_event_3",
        "back_club": "back_club",
        "swipe_up_clubs": "swipe_up_clubs",
        "add_to_hand": "add_to_hand",
        "garage_1_1": "garage_1_1",
        "garage_1_2": "garage_1_2",
        "garage_2_1": "garage_2_1",
        "garage_2_2": "garage_2_2",
        "garage_3_1": "garage_3_1",
        "garage_3_2": "garage_3_2",
        "exit_info": "exit_info",
    }

# * Event action map
event_action_map = {
    'event_1': 'event_1',
    'event_2': 'event_2',
    'event_3': 'event_3',
    'play_event': 'play_event',
    'swipe_left_event': 'swipe_left_event',
}





# * Initialize methods
# Initialize the action map
def initialize_action_map():
    action_map = base_action_map
    action_map.update(club_action_map)
    action_map.update(event_action_map)
    return action_map

# Initialize the check map
def initialize_check_map():
    check_map = base_check_map
    check_map.update(club_check_map)
    check_map.update(event_check_map)
    return check_map


from utils.coords_utils import CoordsUtils
def get_unused_coord_names():
    coordsUtil = CoordsUtils()
    
    coordinates = coordsUtil.coords_data["coordinates"]
    check_map = initialize_check_map()
    action_map = initialize_action_map()
    
   # Define which coordinate categories should belong to which map
    coord_to_map = {
        "box_coords": "action_map",
        "swipe_coords": "action_map",
        "color_coords": "check_map"
    }
    
    # Extract all the coordinate names along with their intended map
    coord_map = {}
    for coord in coordinates["box_coords"]:
        coord_map[coord["name"]] = "action_map"
    for coord in coordinates["swipe_coords"]:
        coord_map[coord["name"]] = "action_map"
    for coord in coordinates["color_coords"]:
        coord_map[coord["name"]] = "check_map"
    
    # Combine all used names in check_map and action_map
    used_names = set(check_map.keys()) | set(action_map.keys())
    
    # Find unused names and their intended map
    unused_coord_info = {
        name: coord_map[name]
        for name in coord_map.keys() - used_names
    }
    
    return unused_coord_info

# unused_coords_info = get_unused_coord_names()
# print("Unused Coordinates and Intended Maps:")
# for name, intended_map in unused_coords_info.items():
#     print(f"{name}: should be in {intended_map}")