from PIL import Image, ImageEnhance, ExifTags
import cv2
import numpy as np
from ImageTools.utils.file_utils import create_dir_if_not_exists


def enhance_contrast(image_path, output_path):
    with Image.open(image_path) as image:
        enhancer = ImageEnhance.Contrast(image)
        enhanced_image = enhancer.enhance(2)  # Adjust factor as needed
        enhanced_image.save(output_path)


def convert_to_grayscale(image_path, output_path):
    with Image.open(image_path).convert('L') as image:
        image.save(output_path)


def binarize_image(image_path, output_path, threshold=128):
    with Image.open(image_path).convert('L') as image:
        binary_image = image.point(lambda p: p > threshold and 255)
        binary_image.save(output_path)


def remove_noise(image_path, output_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised_image = cv2.fastNlMeansDenoising(gray_image, None, 30, 7, 21)
    cv2.imwrite(output_path, denoised_image)



def correct_orientation(image_path):
    # Open the image using PIL to access EXIF data
    with Image.open(image_path) as image:

        # Correct the orientation based on EXIF tags, if present
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            exif = image._getexif()

            if exif is not None:
                orientation = exif.get(orientation, None)
                if orientation == 3:
                    image = image.rotate(180, expand=True)
                elif orientation == 6:
                    image = image.rotate(270, expand=True)
                elif orientation == 8:
                    image = image.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # No EXIF information found
            pass

        # Save the corrected image
        image.save(image_path)


def deskew_image(image_path, output_path, angle_threshold=2):
    # Correct image orientation
    correct_orientation(image_path)

    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect edges in the image
    edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)

    # Use the Hough Transform to find lines
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    if lines is not None:
        angles = []
        for rho, theta in lines[:, 0]:
            angle = np.rad2deg(theta)
            if angle > 90:
                angle -= 180
            angles.append(angle)

        median_angle = np.median(angles)

        if abs(median_angle) < angle_threshold:
            print(f"Skipping rotation, angle too small: {median_angle} degrees")
            cv2.imwrite(output_path, image)
            return

        # Rotate the image
        (h, w) = gray_image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
        rotated_image = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        cv2.imwrite(output_path, rotated_image)
    else:
        # If no lines are detected, save the original image
        # print("No lines detected, skipping deskew.")
        cv2.imwrite(output_path, image)


def enhance_sharpness(image_path, output_path):
    with Image.open(image_path) as image:
        enhancer = ImageEnhance.Sharpness(image)
        enhanced_image = enhancer.enhance(2)  # Adjust factor as needed
        enhanced_image.save(output_path)


def enhance_image(image_path, output_path, denoise: bool = False, deskew: bool = False, grayscale: bool = False,
                        binarize: bool = False, contrast: bool = False, sharpness: bool = False):
    if denoise:
        remove_noise(image_path, output_path)
    else:
        if deskew:
            deskew_image(image_path, output_path)
        else:
            if grayscale:
                convert_to_grayscale(image_path, output_path)
            else:
                if binarize:
                    binarize_image(image_path, output_path)
                else:
                    if contrast:
                        enhance_contrast(image_path, output_path)
                    else:
                        if sharpness:
                            enhance_sharpness(image_path, output_path)
                        else:
                            print("No enhancer selected")
    if deskew:
        deskew_image(output_path, output_path)
    if grayscale:
        convert_to_grayscale(output_path, output_path)
    if binarize:
        binarize_image(output_path, output_path)
    if contrast:
        enhance_contrast(output_path, output_path)
    if sharpness:
        enhance_sharpness(output_path, output_path)
