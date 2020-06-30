import cv2, os
import numpy as np
from utils import *

class ROI():
    def __init__(self,x,y,w,h, defect):
        self.x, self.y = x,y
        self.w, self.h, = w,h
        self.defect = defect

    def __repr__(self):
        return 'ROI: ' + self.getString()

    def getString(self):
        string = "%4.3f %4.3f %4.3f %4.3f %d\n" %(self.x,self.y,self.w,self.h,self.defect)
        return string
    
    def toggleDefect(self, defect):
        if self.defect != defect:
            self.defect = defect
        else:
            self.defect = 0
    
    def isInside(self,x,y):
        if not (self.x <= x <= self.x + self.w):
            return False
        if not (self.y <= y <= self.y + self.h):
            return False
        return True
    
    def plotRectangle(self,image, thickness = 1):
        color = getColorFromDefect(self.defect)
        
        start_point = (int(self.x),int(self.y))
        end_point = (int(self.x + self.w), int(self.y + self.h))

        image = cv2.rectangle(image, start_point, end_point, color, thickness) 

        return image

class ROIArray():
    ROIs = []

    def load(self, filename, image_tuple):
        self.ROIs.clear()
        if not os.path.isfile(filename):
            self.generateROIs(image_tuple)
        else:
            self.parseROIs(filename)

    def save(self,filename):
        if self.ROIs: 
            with open(filename,'w') as file_:
                for elem in self.ROIs:
                    file_.write(elem.getString())

    def generateROIs(self,image_tuple):

        pass

    def toggleDefect(self, x,y, defect):
        for elem in self.ROIs:
            if elem.isInside(x,y):
                elem.toggleDefect(defect)

    def parseROIs(self,filename):
        with open(filename,'r') as file_:
            lines = file_.readlines()
            for line in lines:
                line = line.split(' ')
                if len(line) != 5:
                    raise AssertionError('line must contain 5 elements')
                x,y,w,h,defect = line 
                self.ROIs.append(ROI(float(x),float(y),float(w),float(h),int(defect)))
        print(self.ROIs)
        
    
    def clear(self):
        self.ROIs.clear()
    
    def drawROIs(self,image):
        image
        for roi in self.ROIs:
            image = roi.plotRectangle(image)
        return image
    
    def generateROIs(self, image_tuple):
        image, mask, info  = image_tuple
        for method in ['disk','interdisk']:
            mask_ = getMaskedImage(image, mask, method, True)
            contours, hierarchy = cv2.findContours(mask_[:,:,0].astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for i in range(len(contours)):
                x,y,w,h = cv2.boundingRect(contours[i])
                self.ROIs.append(ROI(float(x),float(y),float(w),float(h),int(0)))
        