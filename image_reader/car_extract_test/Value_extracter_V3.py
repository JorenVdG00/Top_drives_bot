from PIL import Image
import pytesseract
import cv2
import re

# Define expected formats using regular expressions and specific options
patterns = {
    "brand_model": re.compile(r'^[A-Za-z0-9\s]+$'),
    "year": re.compile(r'^(19|20)\d{2}$'),
    "country": re.compile(r'^[A-Za-z]{2}$'),
    "top_speed": re.compile(r'^\d{2,3}$'),
    "0-60": re.compile(r'^\d{1,2}\.\d$'),
    "handling": re.compile(r'^\d{2,3}$'),
    "drive_type": re.compile(r'^(RWD|FWD|4WD)$'),
    "tyres": re.compile(r'^(Performance|Offroad|Standard|Slick|All-Surface)$', re.IGNORECASE),
    "rq": re.compile(r'^\d{2,3}$')
}

# Coords dict with expected formats
coords_dict = {
    "Brand": ([60, 2, 444, 40], "brand_model"),
    "Year": ([447, 1, 500, 37], "year"),
    "Country": ([500, 0, 555, 37], "country"),
    "Top-speed": ([465, 45, 555, 86], "top_speed"),
    "0-60": ([472, 122, 555, 163], "0-60"),
    "Handling": ([480, 200, 555, 240], "handling"),
    "Drive-Type": ([464, 277, 555, 320], "drive_type"),
    "Tyres": ([263, 313, 392, 340], "tyres"),
    "RQ": ([0, 270, 55, 320], "rq")
}

# Load the image
test_img_path = '../Failed_test/test_cropped_imgs/Cars(1,1).png'
image = cv2.imread(test_img_path)
pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

# Initialize an empty dictionary to store the extracted values
extracted_values = {}


# Function to validate and format the extracted text
def validate_and_format(text, pattern_type):
    pattern = patterns[pattern_type]
    if pattern.match(text):
        if pattern_type in {"year", "top_speed", "handling", "rq"}:
            return int(text)
        elif pattern_type == "0-60":
            return float(text)
        elif pattern_type in {"brand_model", "country", "drive_type"}:
            return text.upper()
        elif pattern_type == "tyres":
            return text.title()
    return None


# Extract text from each region specified in coords_dict
for key, (value, pattern_type) in coords_dict.items():
    x, y, x2, y2 = value
    # Crop the image to the region of interest
    cropped_image = image[y:y2, x:x2]

    # Convert the cropped image to PIL format
    pil_cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))

    # Use pytesseract to extract text from the cropped image
    extracted_text = pytesseract.image_to_string(pil_cropped_image, config='--psm 6').strip()

    # Validate and format the extracted text
    formatted_value = validate_and_format(extracted_text, pattern_type)

    # Store the formatted value in the dictionary if it's valid
    if formatted_value is not None:
        extracted_values[key] = formatted_value

# Print the extracted values
for key, value in extracted_values.items():
    print(f"{key}: {value}")

# Optionally display the image with rectangles around the regions
for key, (value, pattern_type) in coords_dict.items():
    x, y, x2, y2 = value
    cv2.rectangle(image, (x, y), (x2, y2), (0, 255, 0), 2)
    cv2.putText(image, key, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
