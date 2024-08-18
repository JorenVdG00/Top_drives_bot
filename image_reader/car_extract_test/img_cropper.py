from PIL import Image

# Load the image
image_path = '../Failed_test/test_IMG/choose_car.png'
image_path_2 = '../Failed_test/test_IMG/pick_cars.png'
img = Image.open(image_path_2)
standard_size = (2210, 1248)
# Define the coordinates for cropping
coordinates = {
    "Cars(1,1)": (640, 248, 1195, 591),
    "Cars(2,1)": (1212, 247, 1769, 590),
    "Cars(1,2)": (638, 610, 1196, 955),
    "Cars(2,2)": (1212, 610, 1768, 955)
}


# Function to resize an image to a standard size
def resize_image(image, standard_size=(2210, 1248)):
    return image.resize(standard_size, Image.Resampling.LANCZOS)


# Function to crop an image based on provided coordinates
def crop_and_save_image(image, coordinates, save_path=None):
    cropped_images = {}
    for car, coords in coordinates.items():
        cropped_image = image.crop(coords)
        cropped_images[car] = cropped_image
        if save_path:
            cropped_image.save(f"{save_path}/{car}.png")
        else:
            cropped_image.save(f"./test_cropped_imgs/{car}.png")
    return cropped_images


resized_img = resize_image(img, standard_size)

# Crop the images based on the resized image
cropped_images = crop_and_save_image(resized_img, coordinates)

# Print the keys (names of the cropped images)
print(cropped_images.keys())  # Listing the names of the cropped images


print("Images have been cropped and saved.")
