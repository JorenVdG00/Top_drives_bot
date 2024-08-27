from PIL import Image
import cv2



# Default global variables
list_coords = []
list_color_coords = []
coords = []
color_coords = []
cropping = False

# Define standard sizes
standard_size_screen = (2210, 1248)
standard_size_cars = (557, 343)  # (cars)
standard_size_events = (330, 220)  # (events)
standard_size_conditions = (315, 85)  # conditions

standard_size = standard_size_screen  # Choose the standard size you're working with


def get_pixel_color(img_path, x, y, standard_size):
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
    img, img_path, list_coords, list_color_coords = param

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
        color = get_pixel_color(img_path, x, y, standard_size)
        cv2.rectangle(img, color_coords[0], (x, y), (25, 255, 25), 2)
        cv2.imshow('image', img)
        list_color_coords.append((color_coords[0], color))


def get_all_coords(img_path: str, standard_size: tuple[int, int]):
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

    Returns:
        tuple:
            - list of all selected rectangular coordinates (list of tuples).
            - dictionary of coordinates and their corresponding RGB color values.
    """
    global list_coords, coords, list_color_coords, color_coords

    img = cv2.imread(img_path)
    resized_img = cv2.resize(img, standard_size, interpolation=cv2.INTER_AREA)
    clone = resized_img.copy()
    list_coords = []  # Reset the list of coordinates
    coords = []  # Reset the current coordinate list
    list_color_coords = []  # Reset the color coordinates list

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', click_and_get_coords, (resized_img, img_path, list_coords, list_color_coords))

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

    print(f"List of selected coordinates: {list_coords}")
    print(f"Coordinates with their colors: {color_dict}")

    return list_coords, color_dict

