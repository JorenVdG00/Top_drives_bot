from garageReader.garage_cropper import get_start_and_crop
from garageReader.garage_reader import read_garage
import os


test_dir = "garageReader\TestGarage\imgs"
test_img1 = os.path.join(test_dir, "test_garage_1.png")
test_img2 = os.path.join(test_dir, "test_garage_2.png")
test_img3 = os.path.join(test_dir, "test_garage_3.png")
test_img4 = os.path.join(test_dir, "test_garage_4.png")
test_img5 = os.path.join(test_dir, "test_garage_5.png")
test_img6 = os.path.join(test_dir, "test_garage_6.png")
test_img7 = os.path.join(test_dir, "test_garage_7.png")



def test_crop_garage():
    get_start_and_crop(test_img1)
    
    
def test_read_garage():
    car_dict = read_garage()
    for key, value in car_dict.items():
        print(key, value)