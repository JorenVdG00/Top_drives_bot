import os
from PIL import Image
from ImageTools import pytesseract
from ImageTools.image_processing.enhancer import enhance_image
from ImageTools.utils.text_utils import clean_race_data, contains_track_name
from ImageTools.utils.file_utils import create_dir_if_not_exists

preprocessing_options = {
    'denoise': [True, False],
    'deskew': [True, False],
    'grayscale': [True, False],
    'binarize': [True, False],
    'contrast': [True, False],
    'sharpness': [True, False]
}


def extract_text_from_image(image_path):
    img = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(img)
    return extracted_text


def extract_event_types(dirs, used_img_dir, enhanced_dir, denoise=False, deskew=False, grayscale=False, binarize=False,
                        contrast=False,
                        sharpness=False, double_lines=False):
    extract_data = {}
    for dir in dirs:
        if dir not in extract_data:
            extract_data[dir] = {}
        files = os.listdir(used_img_dir + dir)
        sorted_files = sorted(files)
        create_dir_if_not_exists(enhanced_dir, dir)
        for file in sorted_files:
            if file in ('conditions.png', 'event_number.png', 'full_race.png'):
                continue
            enhanced_image_path = enhanced_dir + dir + '/' + file
            # enhance_image(used_img_dir + dir + '/' + file, enhanced_image_path, **preprocessing_options)
            enhance_image(used_img_dir + dir + '/' + file, enhanced_image_path, denoise=denoise, deskew=deskew,
                          grayscale=grayscale, binarize=binarize, contrast=contrast, sharpness=sharpness)
            file_name = file.split('.')[0]
            result = extract_text_from_image(enhanced_image_path)
            words = result.replace('\n', ' ').split(' ')
            filtered_words = [word for word in words if word]
            result = ' '.join(filtered_words)

            extract_data[dir][file_name] = result
    return clean_race_data(extract_data)


def run_extraction_with_options(options, faulty_dirs, used_img_dir, enhanced_dir):
    new_extracted_data = extract_event_types(faulty_dirs, used_img_dir, enhanced_dir,
                                             denoise=options['denoise'],
                                             deskew=options['deskew'],
                                             grayscale=options['grayscale'],
                                             binarize=options['binarize'],
                                             contrast=options['contrast'],
                                             sharpness=options['sharpness'])
    return new_extracted_data
