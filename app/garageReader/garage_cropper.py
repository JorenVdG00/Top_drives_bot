from app.utils.ImageTools.image_utils import color_almost_matches
from utils.os_utils import create_dir_if_not_exists
from config import logger, BASIC_WIDTH, BASIC_HEIGHT, TEMP_IMG_DIR, TEMP_GARAGE_DIR, CROPPED_IMG_DIR
import cv2
import os

# # Define the directories
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# TEST_IMG_DIR = os.path.join(BASE_DIR, 'TestGarage')
# TEMP_IMG_DIR = os.path.join(BASE_DIR, 'TempGarage')
# CROPPED_IMG_DIR = os.path.join(TEST_IMG_DIR, 'CroppedCars')

# Create the directories if they don't exist
# create_dir_if_not_exists(TEST_IMG_DIR)
create_dir_if_not_exists(TEMP_IMG_DIR)
create_dir_if_not_exists(CROPPED_IMG_DIR)

# Define color ranges for card separators (as RGB)
target_colors = [
    (113, 184, 229),
    (112, 194, 236),
    (109, 192, 233)
]

#* Useful functions
def get_x_where_vertical_line_is_found(img: cv2, target_color, tolerance=25, required_consecutive=200, start_x = 100, start_y = 100, steps:int = 1):
    """Finds the x-coordinate of the first vertical line of pixels of a given color from the start_x position to the middle of the image.
    
    Args:
        img (cv2): The image to search.
        target_color (tuple): The target RGB color to search for.
        tolerance (int, optional): The tolerance for the color match. Defaults to 25.
        required_consecutive (int, optional): The number of consecutive pixels required to consider it a match. Defaults to 200.
        start_x (int, optional): The x-coordinate to start the search. Defaults to 100.
        start_y (int, optional): The y-coordinate to start the search. Defaults to 100.
        steps (int, optional): The interval between y-coordinates to search. Defaults to 1.
    
    Returns:
        int: The x-coordinate of the first vertical line of pixels, or None if no match is found."""
        
    width, height = img.shape[1], img.shape[0]
    for x in range(start_x, width//2, 5):
        consecutive_count = 0
        for y in range(start_y, height, steps):
            if height - y + (consecutive_count*steps) < required_consecutive:
                break
            pixel_color = tuple(img[y, x])  # Get the pixel color (B, G, R)
            rgb_color = (pixel_color[2], pixel_color[1], pixel_color[0])  # Convert BGR to RGB
            if color_almost_matches(rgb_color, target_color, tolerance):
                consecutive_count += 1
                if consecutive_count >= required_consecutive//steps:
                    return x
            else:
                consecutive_count = 0
    return None


def get_start_and_crop(img_path: str, start_number: int):
    """
    Takes an image path, reads the image, and crops it according to the location of the vertical color line.
    Saves each cropped car image and returns the paths to the saved images.

    Args:
        img_path (str): The path of the image to crop.
        start_number (int): The starting number for the car image filenames.

    Returns:
        list: A list of file paths, each representing a saved cropped car image.
    """
    img = cv2.imread(img_path)

    if img is None:
        print(f"Error loading image at path: {img_path}")
        return False
    else:
        # Resize the image to the base dimensions
        resized_img = cv2.resize(img, (BASIC_WIDTH, BASIC_HEIGHT))
        # Find the x-coordinate of the first vertical line of pixels of the specified color
        start_x = get_x_where_vertical_line_is_found(resized_img, target_colors[0], 25, 700, start_x=20, start_y=100, steps=5)

        # Crop the image into individual car images
        cropped_cars = crop_cars(resized_img, start_x)

        # List to store the paths of the saved images
        saved_img_paths = []

        for index, car in enumerate(cropped_cars):
            # Check if the cropped car image is not too small
            if car.shape[0] > 200 and car.shape[1] > 450:
                # Construct the image file name and path
                img_filename = f'car{index+start_number}.png'
                img_save_path = os.path.join(CROPPED_IMG_DIR, img_filename)

                # Save the cropped image
                save_image(car, img_filename, CROPPED_IMG_DIR)

                # Append the saved image path to the list
                saved_img_paths.append(img_save_path)

        return saved_img_paths
    
def get_start_and_crop_first_four(img_path: str, start_number: int):
    """
    Takes an image path, reads the image, and crops it according to the location of the vertical color line.
    Saves each cropped car image and returns the paths to the saved images.

    Args:
        img_path (str): The path of the image to crop.
        start_number (int): The starting number for the car image filenames.

    Returns:
        list: A list of file paths, each representing a saved cropped car image.
    """
    img = cv2.imread(img_path)

    if img is None:
        print(f"Error loading image at path: {img_path}")
        return False
    else:
        # Resize the image to the base dimensions
        resized_img = cv2.resize(img, (BASIC_WIDTH, BASIC_HEIGHT))
        # Find the x-coordinate of the first vertical line of pixels of the specified color
        start_x = get_x_where_vertical_line_is_found(resized_img, target_colors[0], 25, 700, start_x=20, start_y=100, steps=5)

        # Crop the image into individual car images
        cropped_cars = crop_cars(resized_img, start_x)

        # List to store the paths of the saved images
        saved_img_dirs = []
        nr_cropped_cars = 0
        for index, car in enumerate(cropped_cars):
            # Check if the cropped car image is not too small
            if cropped_cars >= 4:
                break
            if car.shape[0] > 200 and car.shape[1] > 450:
                # Construct the image file name and path
                img_filename = f'car{index+start_number}.png'
                img_save_path = os.path.join(CROPPED_IMG_DIR, img_filename)

                # Save the cropped image
                save_image(car, img_filename, CROPPED_IMG_DIR)

                # Append the saved image path to the list
                saved_img_dirs.append(img_save_path)
                nr_cropped_cars+=1

        return saved_img_dirs
 
def save_image(image, image_name: str,image_path: str):
    """
    Saves an image to a specified path.

    Args:
        image (cv2): The image to save.
        image_name (str): The name of the image file.
        image_path (str): The directory path to save the image in.

    Returns:
        bool: Whether the image was saved successfully.
    """
    path = os.path.join(image_path, image_name)
    return cv2.imwrite(path, image)

def crop_cars(resized_img: cv2, start_x: int = 10):
    carWidth, carHeight = 561, 353
    space_x = 20  # Horizontal space between cards
    space_y = 16  # Vertical space between rows
    x_offset = start_x

    y_top = 242
    y_bottom = y_top + carHeight + space_y

    # Load image
    # img_path = os.path.join(TEST_IMG_DIR, img_list[6])   # Use the desired test image
    # img = cv2.imread(img_path)

    if resized_img is None:
        print(f"Error loading image at path: {resized_img}")
    else:
        # Resize the image to the base dimensions
        # resized_img = cv2.resize(img, (BASIC_WIDTH, BASIC_HEIGHT))

        # Manually calculate card positions based on fixed spaces
        card_positions = []

        # Define the X positions of the cards (using known spacing)
        x_positions = [x_offset]  # Start at x = 0 for the first card
        # for i in range(1, 4):  # There are 3 cards in each row
        while len(x_positions) > 0 and x_positions[-1] < resized_img.shape[1] - carWidth - space_x:
            x_positions.append(x_positions[-1] + carWidth + space_x)

        # Calculate the crop positions for both top and bottom rows
        for x_start in x_positions:
            x_end = x_start + carWidth
            # Crop top row card
            cropped_top_card = resized_img[y_top:y_top + carHeight, x_start:x_end]
            card_positions.append(cropped_top_card)

            # Crop bottom row card
            cropped_bottom_card = resized_img[y_bottom:y_bottom + carHeight, x_start:x_end]
            card_positions.append(cropped_bottom_card)

        # Display the cropped cards
        for idx, card in enumerate(card_positions):
            if card.shape[0] > 0 and card.shape[1] > 0:
                cv2.imshow(f"Cropped Card {idx + 1}", card)
                cv2.waitKey(0)
            else:
                print(f"Card {idx + 1} has invalid dimensions: {card.shape}")

        cv2.destroyAllWindows()
    return card_positions


def crop_car_name(car_img: cv2, save_dir: str, name: str):
   car_img.crop((20,0, 400, 50)).save(os.path.join(save_dir, f'{name}_name.png'))
   
def crop_car_year(car_img: cv2, save_dir: str, name: str):
   car_img.crop((450,0, 540, 40)).save(os.path.join(save_dir, f'{name}_year.png'))