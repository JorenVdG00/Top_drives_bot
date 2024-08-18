from PIL import Image
import pytesseract
import re

# Path to the Tesseract-OCR executable
# Update this path based on your system
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Replace with your actual path

# Load the cropped image
image_path = '../Failed_test/test_cropped_imgs/Cars(1,1).png'
image = Image.open(image_path)

# Extract text from the image using pytesseract
extracted_text = pytesseract.image_to_string(image)

# Define regular expressions to capture the required values
brand_type_regex = r'^[A-Za-z]+\s+[A-Za-z0-9\s-]+'
year_regex = r'\b\d{4}\b'
country_regex = r'\b[A-Z]{2}\b'
topspeed_regex = r'(\d+)\s+TOP\s+SPEED'
zero_sixty_regex = r'(\d+\.\d+)\s+0-60MPH'
handling_regex = r'(\d+)\s+HANDLING'
drivetype_regex = r'\b(RWD|FWD|AWD|4WD)\b'
tyres_type_regex = r'\b(\w+)\s+Tyres\b'
rarity_regex = r'\b[A-Z]\b'
rq_number_regex = r'\b\d+\s+RQ\b'

# Function to safely extract text using regex
def safe_extract(regex, text):
    match = re.search(regex, text)
    return match.group(0) if match else 'N/A'

def safe_extract_group(regex, text, group):
    match = re.search(regex, text)
    return match.group(group) if match else 'N/A'

# Extract values using regular expressions
brand_type = safe_extract(brand_type_regex, extracted_text)
year = safe_extract(year_regex, extracted_text)
country = safe_extract(country_regex, extracted_text)
topspeed = safe_extract_group(topspeed_regex, extracted_text, 1)
zero_sixty = safe_extract_group(zero_sixty_regex, extracted_text, 1)
handling = safe_extract_group(handling_regex, extracted_text, 1)
drivetype = safe_extract(drivetype_regex, extracted_text)
tyres_type = safe_extract_group(tyres_type_regex, extracted_text, 1)
rarity = safe_extract(rarity_regex, extracted_text)
rq_number = safe_extract_group(rq_number_regex, extracted_text, 0).split()[0] if re.search(rq_number_regex, extracted_text) else 'N/A'

# Print the extracted values
print("Brand and Type:", brand_type)
print("Year:", year)
print("Country:", country)
print("Top Speed:", topspeed)
print("0-60 MPH:", zero_sixty)
print("Handling:", handling)
print("Drive Type:", drivetype)
print("Tyres Type:", tyres_type)
print("Rarity:", rarity)
print("RQ Number:", rq_number)


print("Extracted Text:")
print(extracted_text)