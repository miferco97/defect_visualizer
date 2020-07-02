import numpy as np
import cv2, os, pdb, csv 
from utils import *
from dataset_generator import  *
from ROI import *
from cycleLists import *

OPACITY_LEVELS = [0.6, 0.3 , 0 ,1 ]
MODES = ['normal','mask']


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
    showRectangles = True
    
    index = None
    defect_index = None
    mode = CycleList(MODES)
    opacity_level = CycleList(OPACITY_LEVELS)

    def __init__(self, window_name):
        self.window_name = window_name
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name,self.clickCallback)

    def loadImage(self, image_tuple):
        image, mask, info = image_tuple
        self.actual_mask = mask
        self.actual_info = info
        self.actual_defects = info['defect_numbers'] + [0]
        self.defect_index = CycleIndexes(len(self.actual_defects))
        self.actual_filename = getLabelsFilename(info)
        self.ROIarray.load(self.actual_filename,image_tuple)        
        self.actual_image = image
        
    
    def unloadImage(self):
        self.ROIarray.save(self.actual_filename)
        self.ROIarray.clear()
        
    def update(self):
        # img = self.actual_image.copy()
        if self.mode.get() == 'normal':
            img = getMaskedImage(self.actual_image.copy(),self.actual_mask,getAppropiateMask(self.actual_info['defect_numbers']),opacity=self.opacity_level.get())
        elif self.mode.get() == 'mask':
            img = getMaskedImage(self.actual_image.copy(),self.actual_mask,getAppropiateMask(self.actual_info['defect_numbers']),'Original')
        else:
            raise AssertionError('This is not a supported Mode')

        img = drawDefectNames(img,self.actual_info,self.defect_index.get())
        if self.showRectangles:
            img = self.ROIarray.drawROIs(img,self.actual_defects)
        
        cv2.imshow(self.window_name,img)

    def run(self,dataset):
        end = False
        self.index = CycleIndexes(len(dataset))
        while not end:
    
            self.loadImage(dataset[self.index.get()])
        
            if getAppropiateMask(self.actual_defects) == 'None':
                self.index.lastStep()
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
                    self.index.previous()
                    change_image = True
            
                elif c == ord('n'):
                    self.defect_index.next()
                    self.update()
                    # print(self.defect_index)

                elif c == ord('m'):
                    self.mode.next()
                    self.update()

                elif c == ord('o'):
                    self.opacity_level.next()
                    self.update()

                elif c == ord('r'):
                    self.showRectangles= not self.showRectangles
                    self.update()

                elif c == -1:
                    pass                    
                else:
                    self.index.next()
                    change_image = True

            self.unloadImage()


    def clickCallback(self,event,x,y,flags,param):

        if event == cv2.EVENT_LBUTTONDOWN:
            self.ROIarray.toggleDefect(x,y,self.actual_defects[self.defect_index.get()])
            self.update()

    
def main():
    window = UserWindow('test')
    dataset = DefectDataset(BASE_PATH)
    window.run(dataset)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()