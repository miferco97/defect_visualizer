import numpy as np
import cv2, os, pdb, csv 
from utils import *

BASE_PATH = 'Dataset/data_test/'
CSV_FILENAME = 'labels_doc.csv'

class DefectDataset():
    def __init__(self, path, mask_type):
        if mask_type == 'disk' or mask_type == 'interdisk' or mask_type == 'both' :
            self.mask_type = mask_type
        else:
            raise AssertionError("This mask type is not allowed")
        
        self.path = path
        self.image_path = path + 'images/'
        self.labels_path = path + 'labels/'

        self.images = sorted(os.listdir(self.image_path))
        self.images = [image for image in filter(lambda x :  x.endswith('.png') , self.images)]
        self.masks  = sorted(os.listdir(self.labels_path))

        if (len(self.images) != len(self.masks)):
            raise AssertionError(" number of images must be equal to number of labels")
        self.length = len(self.images)
        self.defects = self.readDefects(CSV_FILENAME)

    def __getitem__(self,index):

        defect_row = self.defects[index]
        # print(self.images[i], defect_row['filename'])
        if defect_row['filename'] != self.images[index]:
            raise AssertionError('Both filenames must be equal')
    
        image = cv2.imread(self.image_path  + self.images[index])
        mask  = cv2.imread(self.labels_path + self.masks [index])
        image_filename = self.image_path + self.images[index]

        names, numbers = parseDefectFromBinaryArray(defect_row['defects']) 

        info = { 'defect_names'  : names,
                 'defect_numbers': numbers,
                 'image_filename': image_filename } 

        return (image, mask, info)

    def readDefects(self, filename):
        defects = []
        with open(self.path + filename,mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for i,row in enumerate(csv_reader):
                defect = {'index' : i  , 'filename': row[0] , 'defects': [int(i) for i in row[1:]]}
                defects.append(defect)
        return defects

    

    def __len__(self): 
        return self.length
