from ImageTools.utils.file_utils import get_directories, split_path, create_dir_if_not_exists
from ImageTools.image_processing.extractor import extract_event_types
from ImageTools.image_processing.conditions import get_conditions
from ImageTools.image_processing.faults.fullfill_events import fix_extracted_data


def get_full_correct_list(events_dir):
    sorted_dirs = get_sorted_dirs(events_dir)
    complete_extract_data = get_only_race_tracks(events_dir)

    for dir in sorted_dirs:
        condition_dict = get_conditions(events_dir + dir + '/conditions.png')
        complete_extract_data[dir]['conditions'] = condition_dict

    return complete_extract_data


def get_only_race_tracks(dir):
    enhanced_dir = get_enhanced_dir(dir)
    sorted_dirs = get_sorted_dirs(dir)
    extract_data = extract_event_types(sorted_dirs, dir, enhanced_dir, sharpness=True)
    full_race_type_data = fix_extracted_data(extract_data, dir, enhanced_dir)
    print(full_race_type_data)
    print('now_road_type:::')
    complete_extract_data = fix_extracted_data(full_race_type_data, dir, enhanced_dir, is_race=False)

    return complete_extract_data


def get_enhanced_dir(events_dir):
    base_dir, name = split_path(events_dir)
    enhanced_dir = create_dir_if_not_exists(base_dir, 'enhanced/')
    return enhanced_dir


def get_sorted_dirs(events_dir):
    dirs = get_directories(events_dir)
    sorted_dirs = sorted(dirs)
    return sorted_dirs
