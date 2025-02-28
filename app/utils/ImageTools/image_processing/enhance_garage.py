import cv2

# def get_readable_image(image_path, save_path):
#     img = cv2.imread(image_path)
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     _, result = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY)
#     cv2.imwrite(save_path, result)

def get_readable_image(image_path, save_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # _, result = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)

    adaptive_result = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 1)
    # _, result = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY)
    cv2.imwrite(save_path, adaptive_result)