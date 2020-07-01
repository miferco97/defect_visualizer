import cv2, os
import numpy as np
from utils import *

IGNORE_ZERO_DEFECT = True

class ROI():
    def __init__(self,x,y,w,h, defect, element = None):
        self.x, self.y = x,y
        self.w, self.h, = w,h
        self.defect = defect
        self.object = element

    def __repr__(self):
        return 'ROI: ' + self.getString()
    
    def getObject(self):
        return self.object
    
    def getDefect(self):
        return self.defect

    def getString(self):
        string = "%4.3f %4.3f %4.3f %4.3f %d\n" %(self.x,self.y,self.w,self.h,self.defect)
        return string
    
    def __eq__(self, value):
        result = self.x == value.x  and\
                 self.y == value.y  and\
                 self.w == value.w  and\
                 self.h == value.h
        
        return  result

    def getCenter(self):
        return (self.x + self.w / 2 , self.y + self.h / 2)

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
    
    def plotRectangle(self,image, thickness = 2):
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
            self.ROIs = self.generateROIs(image_tuple)
        else:
            gen_rois = self.generateROIs(image_tuple)    
            parsed_rois = self.parseROIs(filename)
            self.ROIs = self.compareROIs(gen_rois,parsed_rois)
        
    def save(self,filename):
        lines = []
        for roi in self.ROIs:
            if IGNORE_ZERO_DEFECT and roi.getDefect() == 0:
                pass
            else:
                lines.append(roi.getString())
        with open(filename,'w') as file_:
            if lines:
                file_.writelines(lines)

    def toggleDefect(self, x,y, defect):
        clicked_rois = []
        for elem in self.ROIs:
            if elem.isInside(x,y):
                clicked_rois.append(elem)
        if len(clicked_rois) == 1:
            clicked_rois[0].toggleDefect(defect)
        if len(clicked_rois) > 1:
            # TODO implement this method for ease labeling
            pass
             
    def parseROIs(self,filename):
        rois = []
        with open(filename,'r') as file_:
            lines = file_.readlines()
            for line in lines:
                line = line.split(' ')
                if len(line) != 5:
                    raise AssertionError('line must contain 5 elements')
                x,y,w,h,defect = line 
                rois.append(ROI(float(x),float(y),float(w),float(h),int(defect)))
        return rois
    
    def clear(self):
        self.ROIs.clear()
    
    def drawROIs(self,image,actual_defects = [1,2,3,4,5,6]):
        mask = getAppropiateMask(actual_defects)
        for roi in self.ROIs:
            if mask == 'None' or mask == 'both':
                image = roi.plotRectangle(image)
            elif mask == roi.getObject():
                image = roi.plotRectangle(image)  
                
        return image
    
    def generateROIs(self, image_tuple):
        rois = []
        image, mask, info  = image_tuple
        for method in ['disk','interdisk']:
            mask_ = getMaskedImage(image, mask, method, True)
            contours, hierarchy = cv2.findContours(mask_[:,:,0].astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for i in range(len(contours)):
                x,y,w,h = cv2.boundingRect(contours[i])
                rois.append(ROI(float(x),float(y),float(w),float(h),int(0),method))
        return rois

    def compareROIs(self, Rois1, Rois2):
        final_Rois = []
        for roi1 in Rois1:
            roi_unseen = True
            for roi2 in Rois2:
                if roi1 == roi2:
                    if roi1.getObject() != None:
                        element = roi1.getObject()
                    else:
                        element = roi2.getObject()
                    final_Rois.append(ROI(roi1.x,roi1.y,roi1.w,roi1.h,max(roi1.defect,roi2.defect),element))
                    Rois2.remove(roi2)
                    roi_unseen = False
            if roi_unseen:
                final_Rois.append(roi1)                    
        return final_Rois

