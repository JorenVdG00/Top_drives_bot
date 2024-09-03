from ImageTools import track_names, road_type_possibilities


def clean_race_data(extract_data):
    for dir, race_info in extract_data.items():
        race_info['race_type'] = race_info['race_type'].split('\n')[0].strip()
        circuit = race_info['race_type'].split('\n')[0].strip()
        if 'MPH' in circuit:
            circuit = replace_o_with_zero(circuit)
        for road in road_type_possibilities:
            if road in race_info['road_type']:
                race_info['road_type'] = road
        for track in track_names:
            if track in circuit:
                race_info['race_type'] = track
    return extract_data


def replace_o_with_zero(race_str):
    return race_str.replace('O', '0')


def contains_track_name(s):
    for track_name in track_names:
        if track_name in s:
            return track_name
    return None


def fix_missing_space(race_str, possibilities):
    """Attempts to fix missing spaces in a race string based on known possibilities."""

    # Remove spaces to simulate the input with missing spaces
    condensed_race_str = race_str.replace(" ", "")

    for possibility in possibilities:
        if not "MPH" in possibility:
            print(f"Possible missing space in {possibility}")
            continue
        condensed_possibility = possibility.replace(" ", "")
        print(condensed_possibility)
        possibility_0 = replace_o_with_zero(condensed_possibility)
        race_str_0 = replace_o_with_zero(condensed_race_str)
        # Check if the condensed race string matches the condensed possibility
        if possibility_0 == race_str_0:
            return possibility  # Return the correctly formatted possibility

    # If no match is found, return the original string
    return None
