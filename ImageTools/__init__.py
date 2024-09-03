import os
import csv
import pytesseract
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Tesseract path
pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_PATH')

# Load track names and make them available throughout the package
TRACK_NAMES_PATH = os.getenv('TRACK_NAMES_PATH')
track_names = set()

with open(TRACK_NAMES_PATH, mode='r', newline='') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        track_names.add(row[0].strip())

road_type_possibilities = [
    'ASPHALT', 'SNOW', 'DIRT', 'MIXED', 'GRASS', 'SAND', 'ICE', 'GRAVEL'
]

