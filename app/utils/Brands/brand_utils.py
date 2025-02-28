
import csv
from config import car_brands_csv_path

brands_csv_path = car_brands_csv_path

# Method to read car brands from a CSV file
def read_car_brands_from_csv(file_name = brands_csv_path):
    """Reads car brands from a CSV file and returns a list of brands."""
    car_brands = []
    with open(file_name, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            # Each row contains a brand (1 column), so we append it
            car_brands.append(row[0])
    return car_brands


# Method to check if any car brands from the CSV file appear in the text
def find_car_brands_in_str(text):
    """Finds and returns the longest matching car brand from a CSV file in the given text."""
    car_brands = read_car_brands_from_csv()
    text_lower = text.lower()  # Convert text to lowercase for case-insensitive matching

    # Find matching brands
    found_brands = [brand for brand in car_brands if brand.lower() in text_lower]

    if found_brands:
        return max(found_brands, key=len)  # Return the longest matching brand
    return None  # Return None if no brand is found


