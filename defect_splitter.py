import os
import shutil

from tqdm import tqdm

from dataset_generator import *

DESTINY_PATH = './Dataset/data_ree/bent_tower_images/'
COMPLEMENTARY_PATH = './Dataset/data_ree/complementary_images/'
dataset = DefectDataset(BASE_PATH)

try: 
    os.mkdir(DESTINY_PATH)     
except OSError as error: 
    print(error)     

try: 
    os.mkdir(COMPLEMENTARY_PATH)     
except OSError as error: 
    print(error)     

for image, mask , info in tqdm(dataset):
    filename = info['image_filename'].split('/')[-1]
    if 6 in info['defect_numbers']:
        shutil.copy(info['image_filename'],DESTINY_PATH+filename)
    else:
        shutil.copy(info['image_filename'],COMPLEMENTARY_PATH+filename)
