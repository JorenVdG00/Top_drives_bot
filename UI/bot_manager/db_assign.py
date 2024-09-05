import os
import shutil
from database.methods.db_events import get_series, get_races, get_assignees
# from image_reader.event.event_reader_V2 import get_ingame_race_tracks
# from image_reader.event.event_cropper_V3 import crops_ingame_event_types
from ImageTools.Events.event_cropper import crop_event_types
from ImageTools.utils.file_utils import remove_all_files_in_dir, cleanup_dir

from ImageTools.Events.event_reader import get_only_race_tracks
from ImageTools.Events.event_cropper import crop_in_game_event_types
from config import BASE_DIR
def find_matching_serie(event_id, image_path, save_dir=f'{BASE_DIR}/TEMP/'):
    race_dict = {}
    crop_in_game_event_types(image_path, save_dir)
    extracted_races = get_only_race_tracks(save_dir)
    serie_ids = get_series(event_id)


    best_match = None
    highest_match_count = 0

    for serie_id in serie_ids:
        races = get_races(serie_id)
        race_dict[serie_id] = races

        # Compare extracted races with the current series races
        match_count = compare_races(extracted_races, races)
        print(f"Serie {serie_id} has {match_count} matching races.")

        # Update the best match if the current one has more matches
        if match_count > highest_match_count:
            best_match = serie_id
            highest_match_count = match_count
    if best_match:
        print(f"The best matching serie is {best_match} with {highest_match_count} matching races.")
    else:
        print("No matching series found.")
    cleanup_dir(save_dir)
    return best_match

def compare_races(extracted_races, series_races):
    matches = 0
    for race_number, extracted_race in extracted_races.items():
        print(race_number, extracted_race)
        for race_id, race_info in series_races.items():
            if (extracted_race['race_type'] == race_info['name'] and
                    extracted_race['road_type'] == race_info['road_type'] and
                    int(race_number) == int(race_info['number'])):
                matches += 1
                break  # Stop searching for this extracted race once a match is found
    return matches


def check_event_has_assignees(event_id):
    serie_ids = get_series(event_id)
    assignees_dict = {}
    for serie_id in serie_ids:
        assignees = get_assignees(serie_id)
        if not assignees:
            return False
        if len(assignees) < 5:
            return False
        assignees_dict[serie_id] = assignees
    return assignees_dict
def get_corresponding_assignees(event_id, image_path):
    assignees_dict = check_event_has_assignees(event_id)
    if assignees_dict:
        serie_id = find_matching_serie(event_id, image_path)
        if serie_id:
            assignees = assignees_dict[serie_id]
            return assignees
        else:
            return None
    else:
        return None