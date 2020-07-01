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

        self.length = len(self.images)
        self.defects = self.readDefects(CSV_FILENAME)

    def __getitem__(self,index):

        # find index  in CSV
        label_index = None
        for i,row in enumerate(self.defects):
            if row['filename'] == self.images[index]:
                label_index = i
                break
        if label_index is None:
            raise AssertionError('Cant find this filename in ' + CSV_FILENAME)
        
        # find mask
        mask_index = None
        for i,mask_elem in enumerate(self.masks):
            if mask_elem == self.images[index]:
                mask_index = i
                break
        if mask_index is None:
            raise AssertionError('Cant find a mask named in ' + self.images[index])

        
        defect_row = self.defects[label_index]
        
        image_filename = self.image_path + self.images[index]
        
        image = cv2.imread(image_filename)
        mask  = cv2.imread(self.labels_path + self.masks[mask_index])
        
        
        mask = cv2.resize(mask, (image.shape[1],image.shape[0]))
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
