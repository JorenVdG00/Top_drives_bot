from app.utils.ImageTools.image_utils import color_almost_matches, save_cv2_image
from utils.os_utils import create_dir_if_not_exists
from config import logger, BASIC_WIDTH, BASIC_HEIGHT, TEMP_IMG_DIR, TEMP_GARAGE_DIR, CROPPED_IMG_DIR
import cv2
from PIL import Image
import time
import os


# Create the directories if they don't exist
create_dir_if_not_exists(TEMP_IMG_DIR)
create_dir_if_not_exists(TEMP_GARAGE_DIR)
create_dir_if_not_exists(CROPPED_IMG_DIR)


# Define color ranges for card separators (as RGB)
target_colors = [
    (113, 184, 229),
    (112, 194, 236),
    (109, 192, 233)
]

#* Useful functions

def get_x_where_vertical_line_is_found(img: cv2, target_color, tolerance=25, required_consecutive=600, start_x = 100, start_y = 100, steps:int = 1):
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
                print(rgb_color, target_color)
                consecutive_count += 1
                if consecutive_count >= required_consecutive//steps:
                    print(consecutive_count)
                    return x
            else:
                consecutive_count = 0
    return None

def get_start_and_crop(img_path: str, save_path: str = TEMP_GARAGE_DIR):
    """
    Takes an image path, reads the image, and crops it according to the location of the vertical color line.
    Saves each cropped car image and returns the paths to the saved images.

    Args:
        img_path (str): The path of the image to crop.

    Returns:
    Maybe delete
        list: A list of file paths, each representing a saved cropped car image.
    """
    img = cv2.imread(img_path)

    if img is None:
        print(f"Error loading image at path: {img_path}")
        return False
    else:
        # Resize the image to the base dimensions
        resized_img = cv2.resize(img, (BASIC_WIDTH, BASIC_HEIGHT))
        start_x = get_x_where_vertical_line_is_found(resized_img, target_colors[0], 35, 700, start_x=50, start_y=100, steps=5)
        print(start_x)
        cropped_cars = crop_cars(resized_img, start_x)

        saved_dirs = []  # List to store the paths of the saved images

        for index, car in enumerate(cropped_cars):
            car_str = f'car{index+1}'
            crop_car_dir = os.path.join(save_path, car_str)
            
            if car.shape[0] > 200 and car.shape[1] > 450:
                create_dir_if_not_exists(crop_car_dir)
                saved_dirs.append(crop_car_dir)
                # Construct the image file name and path
                img_filename = f'full_{car_str}.png'
                img_save_path = os.path.join(crop_car_dir, img_filename)
                # Save the cropped image
                save_cv2_image(car, img_filename, crop_car_dir)
                # time.sleep(0.5)
                
                with Image.open(img_save_path) as car_img:
                    crop_name_n_year(car_img, crop_car_dir, car_str)

        
        return saved_dirs


def crop_cars(resized_img: cv2, start_x: int = 10):
    carWidth, carHeight = 561, 353
    space_x = 20  # Horizontal space between cards
    space_y = 16  # Vertical space between rows
    x_offset = start_x

    y_top = 242
    y_bottom = y_top + carHeight + space_y

    if resized_img is None:
        print(f"Error loading image at path: {resized_img}")
    else:

        # Manually calculate card positions based on fixed spaces
        card_positions = []

        # Define the X positions of the cards (using known spacing)
        x_positions = [x_offset]  # Start at x = 0 for the first card
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

        #* TO see the cropped cards uncomment the following
        # # Display the cropped cards
        # for idx, card in enumerate(card_positions):
        #     if card.shape[0] > 0 and card.shape[1] > 0:
        #         cv2.imshow(f"Cropped Card {idx + 1}", card)
        #         cv2.waitKey(0)
        #     else:
        #         print(f"Card {idx + 1} has invalid dimensions: {card.shape}")

        # cv2.destroyAllWindows()
    return card_positions


def crop_name_n_year(car_img: Image, save_dir: str, name: str):
    """Crops the car name and year from a given car image and saves them to the given directory.
    
    Args:
        car_img (Image): The car image to crop from.
        save_dir (str): The directory to save the cropped images to.
        name (str): The name of the car to use in the saved filenames.
    
    Returns:
        None
    """
    # Define crop regions for name and year
    name_crop_box = (20, 0, 400, 50)
    year_crop_box = (420, 0, 540, 40)
    
    # Perform cropping
    car_name = car_img.crop(name_crop_box)
    car_year = car_img.crop(year_crop_box)

    # Save the cropped images
    car_name.save(os.path.join(save_dir, f'name_{name}.png'))
    car_year.save(os.path.join(save_dir, f'year_{name}.png'))
