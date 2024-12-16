from ImageTools import track_names, road_type_possibilities
from ImageTools.utils.text_utils import replace_o_with_zero, contains_track_name, clean_race_data
from ImageTools.image_processing.extractor import run_extraction_with_options, preprocessing_options
import itertools


def calculate_percentage_correct_race(extract_data, is_race=True):
    total = 0
    correct = 0
    faults = {}
    if is_race:
        type = 'race_type'
        possibilities = track_names
    else:
        type = 'road_type'
        possibilities = road_type_possibilities
    for dir, races in extract_data.items():
        if races[type]:
            race_type = races[type]
            total += 1
            if race_type in possibilities:
                is_correct = True
                for possibility in possibilities:
                    if possibility not in race_type and race_type in possibility:
                        if dir not in faults:
                            faults[dir] = race_type
                            is_correct = False
                            continue
                if is_correct:
                    correct += 1

            else:
                if dir not in faults:
                    faults[dir] = {}
                faults[dir] = race_type
        else:
            if dir not in faults:
                faults[dir] = {}
            print("No fault detected")
            faults[dir] = None
    if faults == {}:
        print("No faults detected")
        return 1, None
    return correct / total, faults


def get_faulty_dirs(faults):
    faulty_dirs = []
    for dir, fault in faults.items():
        faulty_dirs.append(dir)
    return faulty_dirs


def solve_faults(preprocessing_options, faulty_dirs, used_img_dir, enhanced_dir, is_race=True):
    # Initialize variables
    if is_race:
        type = 'race_type'
        possibilities = track_names

    else:
        type = 'road_type'
        possibilities = road_type_possibilities

    ## Generate all possible combinations of preprocessing options
    combinations = list(itertools.product(*preprocessing_options.values()))

    # Store results
    results = {}

    correct_results = {}
    # Iterate through each combination
    for combination in combinations:
        options = dict(zip(preprocessing_options.keys(), combination))
        print(f"Testing with options: {options}")

        # Run extraction with the current options
        extracted_data = run_extraction_with_options(options, faulty_dirs, used_img_dir, enhanced_dir)
        cleaned_data = clean_race_data(extracted_data)
        # Calculate percentage and faults
        percentage, faults = calculate_percentage_correct_race(cleaned_data, is_race)
        # Delete the correct ones out Faulty Dirs
        if faults is None:
            print('No faults detected')
            break
        else:
            print('Faults:')
            for key, fault in faults.items():
                print(f'{key}: {fault}')
        if not faults:
            for key in faulty_dirs:
                correct_results[key] = cleaned_data[key][type]
                faulty_dirs.remove(key)
        else:
            for key in faulty_dirs:
                print(key)
                if key not in faults:
                    print(f'{key}')
                    print(extracted_data[key])
                    correct_results[key] = cleaned_data[key][type]
                    faulty_dirs.remove(key)
                else:
                    if is_race:
                        if type == 'race_type':
                            track_name = contains_track_name(cleaned_data[key][type])
                            if track_name:
                                correct_results[key] = track_name
                                faulty_dirs.remove(key)
                                continue

                    for possible in possibilities:
                        if faults[key] and possible in faults[key]:  # Ensure faults[key] is iterable
                            correct_results[key] = possible
                            faulty_dirs.remove(key)
                            break

        # Store the results
        results[str(options)] = {'percentage': percentage, 'faults': faults}
    return correct_results


def change_data_to_correct_results(extract_data, correct_results, is_race=True):
    if is_race:
        type = 'race_type'
    else:
        type = 'road_type'
    for dir in correct_results:
        extract_data[dir][type] = correct_results[dir]
    return extract_data


def fix_extracted_data(extract_data, used_img_dir, enhanced_img_dir, is_race=True):
    percentage, faults = calculate_percentage_correct_race(extract_data, is_race)
    print(faults)
    if faults:
        faulty_dir = get_faulty_dirs(faults)
        correct_results = solve_faults(preprocessing_options, faulty_dir, used_img_dir, enhanced_img_dir, is_race)
        print(correct_results)
        print("Changing faults data to correct results")
        extract_data = change_data_to_correct_results(extract_data, correct_results, is_race)
    else:
        print("No faults found")
    return extract_data

