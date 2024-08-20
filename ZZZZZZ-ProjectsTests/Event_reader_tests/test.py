# event_img_coords = {
#     "race_type" : (5,5,320,50),
#     "conditions" : (5,60,320,145),
#     "event_number": (0,150,65,215),
#     "road_type": (75,150,330,215)
# }
#
#
#
# for xcoords in event_img_coords.values():
#     print(xcoords)
#
# for keys, coords in event_img_coords.items():
#     print(keys,coords)
#
#

import os


#
def split_path(path):
    # Remove trailing slashes if any
    path = path.rstrip('/')

    # Split the path into head (rest of the path) and tail (last directory name)
    head, tail = os.path.split(path)
    return head, tail


###DIRECTORIES###
test1_dir = 'AAAA/event_test_V2_cropped/RACING_TRIALS_-_STAGE_2'
test2_dir = 'AAAA/event_test_V2_cropped/RACING_TRIALS_-_STAGE_2/'
base_dir, name = split_path(test1_dir)
print(base_dir, 30*'*', name)
print(test2_dir)
base_dir, name = split_path(test2_dir)
print(base_dir, 30*'*',  name)

enhanced_dir = base_dir+ "/" + (name + '_enhanced/')
print(enhanced_dir)

