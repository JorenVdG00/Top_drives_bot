from PIL import Image
import numpy as np

# Function to resize an image to a standard size
def resize_image(image, standard_size=(335, 245)):
    return image.resize(standard_size, Image.Resampling.LANCZOS)


def calculate_pixel_similarity(image1_path, image2_path):
    # Open and convert images to grayscale
    img1 = Image.open(image1_path).convert('L')
    img1 = resize_image(img1)
    img2 = Image.open(image2_path).convert('L')
    img2 = resize_image(img2)
    # Ensure images are the same size
    if img1.size != img2.size:
        raise ValueError("Images must be the same size")

    # Convert images to numpy arrays
    arr1 = np.array(img1)
    arr2 = np.array(img2)

    # Calculate the number of matching pixels
    matching_pixels = np.sum(arr1 == arr2)
    total_pixels = arr1.size

    # Calculate the similarity percentage
    similarity_percentage = (matching_pixels / total_pixels) * 100
    return similarity_percentage

# Example usage
image1_path = 'event_test/HEAVY_HITTERS/1-2.png'
image2_path = '../../ZZZZZ-TEST-IIIIIIIIMG/In_game_cropped/In_game_cropped-5.png'


similarity = calculate_pixel_similarity(image1_path, image2_path)
print(f"Pixel-wise similarity: {similarity:.2f}%")
