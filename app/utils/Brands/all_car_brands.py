from bs4 import BeautifulSoup
import requests
import re
import csv

url = "https://top-drives.fandom.com/wiki/Cars"

page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

# Find the specific div with the class "mw-parser-output"
content_div = soup.find("div", class_="mw-parser-output")

# Function to clean and split brand names based on the rules
def clean_brand_name(brand_name) -> list[str]:
    # Remove any text inside parentheses
    brand_name = re.sub(r'\s*\(.*?\)\s*', '', brand_name).strip()
    
    # If there is a "/", split the name into multiple brands
    if '/' in brand_name:
        return [b.strip() for b in brand_name.split('/')]
    
    return [brand_name]

def write_list_to_csv(list_to_write, filename):
    """Writes a list to a CSV file, each item on a new line."""
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in list_to_write:
            writer.writerow([item])

car_brands = []
car_brands.append("Apollo")  # Special case
car_brands.append("Morgan")  # Special case

for li in content_div.find_all("li"):
    if 'game' in li.text.lower(): continue

    brands = clean_brand_name(li.text)
    car_brands.extend(brands)

write_list_to_csv(car_brands, 'Top_drives_bot/car_brands.csv')
