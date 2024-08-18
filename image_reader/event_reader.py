from PIL import Image
import pytesseract
import re
import os
from image_enhancer import (full_image_enhancer)

image_path = 'Failed_test/crop_events/name.png'
img_path = 'Failed_test/event_test/HEAVY_HITTERS/1-1.png'
img_path2 = './event_test/HEAVY_HITTERS/1-4.png'
img_path3 = './event_test/In_game_cropped/In_game_cropped-5.png'
# img_path2 = './event_test/HEAVY_HITTERS/1-2.png'
IMG_DIR = 'Failed_test/event_test/HEAVY_HITTERS/'
IMG_DIR_INGAME = 'Failed_test/event_test/In_game_cropped/'
enhanced_dir = 'Failed_test/event_test/ENHANCED/'
#
extract_data = {}
files = os.listdir(IMG_DIR)
print(files)
sorted_files = sorted(files)
print(sorted_files)
for file in sorted_files:
    full_image_enhancer(IMG_DIR + file, enhanced_dir + file, denoise=True,deskew=True, grayscale=False, binarize=False, contrast=False)
    img = Image.open(enhanced_dir + file)
    fname = file.split('.')[0]
    extracted_text = pytesseract.image_to_string(img)
    # print(extracted_text)
    extract_data[fname] = extracted_text

print(extract_data)

print(50 * '*')
full_image_enhancer(img_path3, 'Failed_test/final_result_img/test.png', contrast=True, grayscale=False, binarize=False,
                    denoise=True, deskew=True)
img = Image.open('Failed_test/final_result_img/test.png')
extracted_text = pytesseract.image_to_string(img)
print(extracted_text)

# extracted_text = pytesseract.image_to_string(img)
# print(extracted_text)


# print("Extracted Text:", extracted_text[:-1])
