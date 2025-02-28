from config import pytesseract, BASIC_HEIGHT, BASIC_WIDTH, logger
from garageReader.garage_cropper import get_start_and_crop, CROPPED_IMG_DIR
from ImageTools.extractors.extractor_garage import run_text_extraction_with_10_combinations
from utils.os_utils import get_files, get_directories
from scraper.car_scraper import scrape_car
from PIL import Image
import os



def is_year_pattern(string):
    try:
        year = int(string)
        if 1900 <= year <= 2100:
            return True
        else:
            return False
    except ValueError:
        return False
    
def find_year(string):
    
    if is_year_pattern(string):
        return string
    else:
        return None
    

def read_garage(car_dirs):
    found_cars = []
    
    for car_dir in car_dirs:
        car_dir_name = os.path.basename(car_dir)
        
        car_name_path = os.path.join(car_dir, f"name_{car_dir_name}.png")
        car_year_path = os.path.join(car_dir, f"year_{car_dir_name}.png")
        save_path = os.path.join(car_dir, f"enh_{car_dir_name}.png")
        
        car = run_text_extraction_with_10_combinations(car_name_path, car_year_path, save_path)
        
        if car["brand"] != None:
            found_car =scrape_car(car["brand"], car["type"], car["year"])
            found_cars.append(found_car)
    return found_cars    

def extract_car_info(img_dir):
    """
    Extracts the car brand, type and year from the given directory which contains 
    the car name and year images. The extracted information is saved in a dictionary
    and returned.

    Args:
        img_dir (str): The directory containing the car name and year images.

    Returns:
        dict: A dictionary containing the extracted car brand, type, and year.
    """
    car_dir_name = os.path.basename(img_dir)
    
    car_name_path = os.path.join(img_dir, f"name_{car_dir_name}.png")
    car_year_path = os.path.join(img_dir, f"year_{car_dir_name}.png")
    save_path = os.path.join(img_dir, f"enh_{car_dir_name}.png")
    
    # Saves car as {brand: ...., type: ...., year: ....}
    car = run_text_extraction_with_10_combinations(car_name_path, car_year_path, save_path)
    return car


    
    
# def read_garage(cropped_cars_dir = CROPPED_IMG_DIR):
#     car_dict = {}
    
#     cars = get_files(cropped_cars_dir)
    
#     for car in cars:
#         car_path = os.path.join(cropped_cars_dir, car)
        
#         with Image.open(car_path) as car_image:
#             car_name = car_image.crop((20,0, 400, 50))
#             car_name.save(os.path.join(cropped_cars_dir, f'name_{car}'))
#             extract_name = pytesseract.image_to_string(car_name)
#             car_year = car_image.crop((450,0, 540, 40))
#             car_year.save(os.path.join(cropped_cars_dir, f'year_{car}'))
#             # while extract_year == 
#             extract_year = pytesseract.image_to_string(car_year)
#             car_dict[extract_name] = extract_year
#     return car_dict


