from PIL import Image
import re

standard_size = (2210, 1248)

event_coordinates = {
    "name": (650, 270, 1550, 350),
    "event_x": {
        "event_x_1": (175, 510),
        "event_x_2": (560, 900),
        "event_x_3": (940, 1280),
        "event_x_4": (1310, 1660),
        "event_x_5": (1710, 2050)
    },
    "event_y": {
        "event_y_1": (470, 715),
        "event_y_2": (850, 1060),
        "event_y_3": (570, 820),
        "event_y_4": (940, 1160)
    },
    "in_game_event_x": {
        "in_game_event_x_1": (210, 510),
        "in_game_event_x_2": (580, 880),
        "in_game_event_x_3": (950, 1250),
        "in_game_event_x_4": (1320, 1625),
        "in_game_event_x_5": (1700, 2000)
    },
    "in_game_event_y": (530, 745)
}


# Function to classify the filenames
def classify_filename(filename):
    patterns = {
        '1': r'1-2\.png',
        '3': r'3-4\.png',
        'in_game': r'in_game\.png'
    }

    for category, pattern in patterns.items():
        if re.search(pattern, filename):
            print(f"Found {filename} in category {category}")
            return category
    return "No match"


# Function to resize an image to a standard size
def resize_image(image, standard_size=(2210, 1248)):
    return image.resize(standard_size, Image.Resampling.LANCZOS)


def crop_and_save_event_type_images(img_path, save_dir):
    category = classify_filename(img_path)
    print(category)
    cropped_images = {}
    image = Image.open(img_path)
    image = resize_image(image, standard_size)

    if category == 'No match':
        print(f"No match found for {img_path}")
        return
    if category == 'in_game':
        y1, y2 = event_coordinates['in_game_event_y']
        print(y1, y2)
        i=1

        for xcoords in event_coordinates['in_game_event_x'].values():
            for x1, x2 in xcoords:
                cropped_image = image.crop((x1, y1, x2, y2))
                cropped_images[i] = cropped_image
                cropped_image.save(f"{save_dir}/{category}-{i}.png")
                i+=1
    elif category == '1':
        name_coords = event_coordinates['name']
        cropped_image = image.crop(name_coords)
        cropped_images["name"] = cropped_image
        cropped_image.save(f"{save_dir}/name.png")
        i=1
        y1, y2 = event_coordinates['event_y']['event_y_1']
        for xcoords in event_coordinates['event_x'].values():
            x1, x2 = xcoords
            cropped_image = image.crop((x1, y1, x2, y2))
            cropped_images["1"] = cropped_image
            cropped_image.save(f"{save_dir}/{category}-{i}.png")
            i+=1

        y1, y2 = event_coordinates['event_y']['event_y_2']
        i=1
        for xcoords in event_coordinates['event_x'].values():
            x1, x2 = xcoords
            cropped_image = image.crop((x1, y1, x2, y2))
            cropped_images["2"] = cropped_image
            cropped_image.save(f"{save_dir}/{int(category)+1}-{i}.png")
            i+=1

    elif category == '3':
        i=1

        y1, y2 = event_coordinates['event_y']['event_y_3']
        for xcoords in event_coordinates['event_x'].values():
            x1, x2 = xcoords
            cropped_image = image.crop((x1, y1, x2, y2))
            cropped_images["3"] = cropped_image
            cropped_image.save(f"{save_dir}/{category}-{i}.png")
            i+=1

        y1, y2 = event_coordinates['event_y']['event_y_4']
        i=1
        for xcoords in event_coordinates['event_x'].values():
            x1, x2 = xcoords
            cropped_image = image.crop((x1, y1, x2, y2))
            cropped_images["4"] = cropped_image
            cropped_image.save(f"{save_dir}/{int(category)+1}-{i}.png")
            i+=1
    return cropped_images


org_img = Image.open('../../ZZZZZ-TEST-IIIIIIIIMG/test/event_types1-2.png')
resized_img = resize_image(org_img)

crop_and_save_event_type_images('test_IMG/large_name_1-2.png', 'Failed_test/crop_events')



