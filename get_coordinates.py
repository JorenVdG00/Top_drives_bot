import os
from utils.find_coords_n_colors import get_all_coords, get_pixel_color
from config import BASIC_WIDTH, BASIC_HEIGHT

STANDARD_SCREEN_SIZE = (BASIC_WIDTH, BASIC_HEIGHT)

# STANDARD_sizes
new_size = (1600, 900)
new_size2 = (1400, 700)


img_dir = './Z_FIND_COORDS_IMG/'
my_cars_path = os.path.join(img_dir, 'Mycars.png')


if __name__ == '__main__':
    # # Example to get all coordinates for a box or a color for a certain spot
    # #* Hold and RELEASE LMB to get box_coords, MMB to get coords, color at certain loc
    # get_all_coords(my_cars_path, new_size2, STANDARD_SCREEN_SIZE)
    # #
    # #Example get pixel_Color at coords
    # get_pixel_color(my_cars_path, 150, 800, STANDARD_SCREEN_SIZE)
    list_a = ["Joren", "Jarne", "Kyara"]
    print(list_a)
    name = f"{' '.join(list_a[:3])}"
    print(name)
    list_a[2] = list_a[2][:-1]
    print(list_a)
    
    test_string = "Bugatti Divo 2022"
    brand = "Bugatti"
    model = test_string.replace(brand, "").strip()
    print(f"-{model}-")