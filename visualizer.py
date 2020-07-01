import numpy as np
import cv2, os, pdb, csv 
from utils import *
from dataset_generator import  *
from ROI import *

def getLabelsFilename(info):
    filename = info['image_filename']
    filename = filename.replace('.png', '.txt')
    return filename

class UserWindow():
    ROIarray = ROIArray()
    actual_filename = ''
    actual_image = None
    actual_defects  = []
    actual_info = None
    index = 0
    mode = 'normal'
    defect_index = 0
    index_dif = +1

    def __init__(self, window_name):
        self.window_name = window_name
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name,self.clickCallback)

    def loadImage(self, image_tuple):
        image, mask, info = image_tuple
        self.actual_mask = mask
        self.actual_info = info
        self.actual_defects = info['defect_numbers'] + [0]
        self.actual_filename = getLabelsFilename(info)
        self.ROIarray.load(self.actual_filename,image_tuple)        
        self.actual_image = image
        
    
    def unloadImage(self):
        self.defect_index = 0
        self.ROIarray.save(self.actual_filename)
        self.ROIarray.clear()
        
    def update(self):
        img = self.actual_image.copy()

        if self.mode == 'normal':
            img = getMaskedImage(img,self.actual_mask,getAppropiateMask(self.actual_info['defect_numbers']))
        if self.mode == 'mask':
            img = getMaskedImage(img,self.actual_mask,getAppropiateMask(self.actual_info['defect_numbers']),True)

        img = drawDefectNames(img,self.actual_info,self.defect_index)
        img = self.ROIarray.drawROIs(img,self.actual_defects)
        
        cv2.imshow(self.window_name,img)

    def toggleMode(self):
        if  self.mode == 'normal':
            self.mode = 'mask'
        else:
            self.mode = 'normal'

    def run(self,dataset):
        end = False
        while not end:

            if self.index >= len(dataset):
                self.index = 0
            elif self.index < 0:
                self.index = len(dataset) + self.index

            # cycle indexes
            self.loadImage(dataset[self.index])
            
            if getAppropiateMask(self.actual_defects) == 'None':
                change_image = True
                print (self.actual_filename + ' does not have any defects')
            else:
                self.update()
                print (self.actual_filename)
                change_image = False

            while not change_image:
                c = cv2.waitKey(30)
                if c == 27:
                    #click ESC to exit
                    end = True
                    break

                elif c == ord('b'):
                    #click  B to go previous image
                    self.index_dif = -1
                    change_image = True
            
                elif c == ord('n'):
                    self.defect_index += 1
                    if self.defect_index >= len(self.actual_defects):
                        self.defect_index = 0
                    self.update()
                    # print(self.defect_index)

                elif c == ord('m'):
                    self.toggleMode()
                    self.update()


                elif c == -1:
                    pass                    
                else:
                    self.index_dif = +1
                    change_image = True

            self.unloadImage()
            self.index += self.index_dif


    def clickCallback(self,event,x,y,flags,param):

        if event == cv2.EVENT_LBUTTONDOWN:
            self.ROIarray.toggleDefect(x,y,self.actual_defects[self.defect_index])
            self.update()

    
def main():
    window = UserWindow('test')
    dataset = DefectDataset(BASE_PATH, 'both')
    window.run(dataset)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()