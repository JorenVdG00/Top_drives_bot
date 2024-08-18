from PIL import Image
import pytesseract
import cv2
import numpy as np

# Standard size for the image
standard_size = (557, 343) #(cars)


# Coords dict
coords_dict = {
    "Brand": [60, 2, 444, 40],
    "Year": [447, 1, 500, 37],
    "Country": [500, 0, 555, 37],
    "Top-speed": [465, 45, 555, 86],
    "0-60": [472, 122, 555, 163],
    "Handling": [480, 200, 555, 240],
    "Drive-Type": [464, 277, 555, 320],
    "Tyres": [263, 313, 392, 340],
    "RQ": [0, 270, 55, 320]
}

# Load the image
test_img_path = '../Failed_test/test_cropped_imgs/Cars(1,1).png'
image = cv2.imread(test_img_path)
pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


# Use pytesseract to get detailed data
data = pytesseract.image_to_data(pil_image, output_type=pytesseract.Output.DICT)




for key, value in coords_dict.items():
    x, y, w, h = value[0], value[1], value[2] - value[0], value[3] - value[1]
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(image, key, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

cv2.imshow('image', image)
cv2.waitKey(0)











# new_dict = {}
# for key, value in coords_dict.items():
#     new_dict[key]['x'] = value[0]
#     new_dict[key]['y'] = value[1]
#     new_dict[key]['w'] = value[2] - value[0]
#     new_dict[key]['h'] = value[3] - value[1]
# print(new_dict)
