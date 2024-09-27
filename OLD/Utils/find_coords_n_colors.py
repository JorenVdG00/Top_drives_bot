from PIL import Image
import cv2
from config import BASIC_WIDTH, BASIC_HEIGHT

STANDARD_SCREEN_SIZE = (BASIC_WIDTH, BASIC_HEIGHT)

# STANDARD_sizes
new_size = (1600, 900)
new_size2 = (1400, 700)
standard_size_screen = (2210, 1248)
standard_size_cars = (557, 343)  # (cars)
standard_size_events = (330, 220)  # (events)
standard_size_conditions = (315, 85)  # conditions

# Default global variables
list_coords = []
list_color_coords = []
coords = []
color_coords = []
cropping = False


def get_pixel_color(img_path, x, y, standard_size=STANDARD_SCREEN_SIZE):
    """
    Get the color of a specific pixel in the image.

    Args:
        img_path (str): Path to the image file.
        x (int): X-coordinate of the pixel.
        y (int): Y-coordinate of the pixel.
        standard_size (tuple[int, int]): The desired size to which the image will be resized
                                         before extracting the color.

    Returns:
        tuple: RGB color value of the specified pixel.
    """
    img = Image.open(img_path)
    resized_img = img.resize(standard_size)
    return resized_img.getpixel((x, y))


def click_and_get_coords(event, x, y, flags, param):
    """
    Mouse callback function to capture coordinates on mouse click and drag.

    - Left Mouse Button:
        - Press and drag to select a rectangular region. The top-left and bottom-right coordinates of the
          rectangle are stored, and the rectangle is drawn on the image.
    - Middle Mouse Button:
        - Click to capture the coordinate and the color at that point. The coordinate and its corresponding
          color are stored and a small rectangle is drawn at that point.

    Args:
        event: Mouse event type (e.g., button down, button up).
        x: X-coordinate of the mouse event.
        y: Y-coordinate of the mouse event.
        flags: Additional flags (not used here).
        param: Tuple containing the image and lists to store coordinates and colors.
    """
    global coords, color_coords, cropping
    img, img_path, list_coords, list_color_coords, size = param

    if event == cv2.EVENT_LBUTTONDOWN:
        coords = [(x, y)]
        cropping = True
    elif event == cv2.EVENT_LBUTTONUP:
        coords.append((x, y))
        cropping = False
        cv2.rectangle(img, coords[0], coords[1], (0, 255, 0), 2)
        cv2.imshow('image', img)
        list_coords.append(coords)
    elif event == cv2.EVENT_MBUTTONDOWN:
        color_coords = [(x, y)]
    elif event == cv2.EVENT_MBUTTONUP:
        # Get color at the clicked point
        color = get_pixel_color(img_path, x, y, size)
        cv2.rectangle(img, color_coords[0], (x, y), (25, 255, 25), 2)
        cv2.imshow('image', img)
        list_color_coords.append((color_coords[0], color))


def get_all_coords(img_path: str, size: tuple[int, int], retune_size: tuple[int, int] = STANDARD_SCREEN_SIZE):
    """
    Display an image and allow the user to interact with it to select regions and colors.

    - Left Mouse Button:
        - Click and drag to select rectangular regions. The coordinates of the selected regions are saved.
    - Middle Mouse Button:
        - Click to capture the coordinate and the color at that point. The coordinate and its corresponding
          color are saved.

    Args:
        img_path (str): Path to the image file.
        standard_size (tuple[int, int]): Desired size to resize the image for processing.
        retune_size = tuple[int, int]: This is used when size is too big for pc screen,
                      You take a lower size and at the end it will recalculate for your retune_size size.
                      STANDARD_SCREEN_SIZE is the one all coords are configured on,


    Returns:
        tuple:
            - list of all selected rectangular coordinates (list of tuples).
            - dictionary of coordinates and their corresponding RGB color values.
    """
    global list_coords, coords, list_color_coords, color_coords

    img = cv2.imread(img_path)
    resized_img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
    clone = resized_img.copy()
    list_coords = []  # Reset the list of coordinates
    coords = []  # Reset the current coordinate list
    list_color_coords = []  # Reset the color coordinates list

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', click_and_get_coords,
                         (resized_img, img_path, list_coords, list_color_coords, size))

    while True:
        cv2.imshow("image", resized_img)
        key = cv2.waitKey(1) & 0xFF

        # Press 'r' to reset the window
        if key == ord("r"):
            resized_img = clone.copy()
            list_coords = []
            list_color_coords = []
            coords = []
            color_coords = []

        # If the 'q' key is pressed, break from the loop
        elif key == ord("q"):
            break

    cv2.destroyAllWindows()

    color_dict = {coord[0]: coord[1] for coord in list_color_coords}



    retuned_coords = retune_coords(list_coords, size, retune_size)
    retuned_colors_dict = retune_coords(color_dict, size, retune_size, is_color=True)

    print(f"List of selected coordinates: {retuned_coords}")
    print(f"Coordinates with their colors: {retuned_colors_dict}")
    return retuned_coords, retuned_colors_dict




def retune_coords(coords, size, retune_size, is_color = False):
    x_retune_value, y_retune_value = retune_size[0]/size[0], retune_size[1]/size[1]
    if is_color:
        retuned_color_coords_dict = {}
        for coord, color in coords.items():
            retuned_color_coords = int(coord[0]*x_retune_value), int(coord[1]*y_retune_value)
            retuned_color_coords_dict[retuned_color_coords] = color
        return retuned_color_coords_dict
    else:
        retuned_coords = []
        for coords_list in coords:
            coords_temp_list = []
            for coords_tuple in coords_list:
                coord_x, coord_y = int(coords_tuple[0]*x_retune_value), int(coords_tuple[1]*y_retune_value)
                coords_temp_list.append((coord_x, coord_y))
            retuned_coords.append(coords_temp_list)
        return retuned_coords



if __name__ == '__main__':
    img_path = 'IMG/cars1.png'
    img_path2 = './IMG/cars_need_repair.png'
    club_home = './IMG/out_club_play.png'
    in_club_event = './IMG/in_club_event_cropper2.png'
    add_to_hand = './IMG/in_event_play.png'

    get_all_coords(add_to_hand, new_size2, STANDARD_SCREEN_SIZE)
    # 226, 226, 227, 255    1966, 162   ASC
    # 254, 254, 254, 255    1966, 180   DOWN
    # print(get_pixel_color(add_to_hand, 250, 798, STANDARD_SCREEN_SIZE))
    # print(get_pixel_color(img_path, 580, 1080, STANDARD_SCREEN_SIZE))
    # print(get_pixel_color(img_path, 930, 1080, STANDARD_SCREEN_SIZE))
    # print(get_pixel_color(img_path, 1280, 1080, STANDARD_SCREEN_SIZE))
    # print(get_pixel_color(img_path, 1630, 1080, STANDARD_SCREEN_SIZE))

    # print(get_pixel_color(club_home, 1280, 614, new_size))
    # print('ASC COLOR, ', get_pixel_color(asc_path, 1966, 163, STANDARD_SCREEN_SIZE))
    # print('DESC COLOR, ', get_pixel_color(desc_path, 1966, 181, STANDARD_SCREEN_SIZE))
    #
    # print('ASC COLOR on sort, ', get_pixel_color(sort_path, 1966, 163, STANDARD_SCREEN_SIZE))
    # print('DESC COLOR on sort, ', get_pixel_color(sort_path, 1966, 181, STANDARD_SCREEN_SIZE))

