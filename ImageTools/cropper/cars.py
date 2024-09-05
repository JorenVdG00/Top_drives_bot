from ImageTools.cropper.coords import car_coords
from ImageTools.image_processing.cropper import crop_image


def crop_all_hand_cars(image_path, save_dir):
    std_x1, y1, x2, y2 = car_coords['coords']
    step = car_coords['step']
    width = x2 - std_x1
    for car_number in range(1, 6):
        x1 = std_x1 + ((car_number - 1) * (width + step))
        x2 = x1 + width
        coords = (x1, y1, x2, y2)
        crop_image(image_path, save_dir, f'car{car_number}', coords)
