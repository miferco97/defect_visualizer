import cv2, os
import numpy as np
from utils import *

IGNORE_ZERO_DEFECT = False
MINIMUM_ROI_AREA = 0.01 # In image proportion

class ROI():
    def __init__(self,x,y,w,h, defect, element = None):
        self.x, self.y = x,y
        self.w, self.h, = w,h
        self.defect = defect
        self.object = element
        self.active = True
        self.checkArea()
        
        # print(element)
        
        if defect is None:
            if element == 'disk':
                self.defect = -1
            elif element == 'interdisk':
                self.defect = -2
            # else:
            #     raise AssertionError ('this method is not handled properly')
                
    def checkArea(self):
        last_active = self.active
        if MINIMUM_ROI_AREA:
            if last_active == True:     
                area = self.w * self.h
                if area < MINIMUM_ROI_AREA:
                    self.active = False
                else:
                    self.active = True
            
    def setActive(self, value):
        if not (type(value) is bool):
            raise AssertionError ('active value must be boolean')
        self.active = value
        self.checkArea()

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

    def getCenter(self,image_size = None):
        if image_size is None:
            return (self.x + self.w / 2 , self.y + self.h / 2)
        else:
            return ((self.x + self.w / 2)*image_size[1], (self.y + self.h / 2)*image_size[0])


    def toggleDefect(self, defect):
        if self.active:
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
        if self.active:
            color = getColorFromDefect(self.defect)            
            start_point = (int(self.x),int(self.y))
            end_point = (int(self.x + self.w), int(self.y + self.h))
            
            image = cv2.rectangle(image, start_point, end_point, color, thickness) 

        return image

class ROIArray():
    ROIs = []

    def load(self, filename, image_tuple):
        image_size = image_tuple[0].shape
        # print(image_size)
        # TODO 
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
            
            if elem.active and elem.isInside(x,y):
                clicked_rois.append(elem)
        if len(clicked_rois) == 1:
            clicked_rois[0].toggleDefect(defect)

        if len(clicked_rois) > 1:
            min_center_distance = np.inf
            for roi in clicked_rois:
                center_x,center_y = roi.getCenter()
                distance = (x-center_x)**2 + (y-center_y)**2
                if distance < min_center_distance:
                    min_center_distance = distance
                    candidate = roi
            if candidate:
                candidate.toggleDefect(defect)
             
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
    

    def activateROIs(self):
        for roi in self.ROIs:
            roi.setActive(True)
    
    def deactivateROIs(self):
        for roi in self.ROIs:
            roi.setActive(False)
    
    def activeObjectROIs(self, tag):
        for roi in self.ROIs:
            if tag == 'both' or roi.getObject() == tag:
                roi.setActive(True)
            else:
                roi.setActive(False)
            

    def drawROIs(self,image,actual_defects = [-1,-2, 1,2,3,4,5,6]):
        mask = getAppropiateMask(actual_defects)
        self.activeObjectROIs(mask)
        for roi in self.ROIs:
            image = roi.plotRectangle(image)
                
        return image
    
    def generateROIs(self, image_tuple):
        rois = []
        image, mask, info  = image_tuple
        for method in ['disk','interdisk']:
            mask_ = getMaskedImage(image, mask, method, 'filtered')
            contours, hierarchy = cv2.findContours(mask_[:,:,0].astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for i in range(len(contours)):
                x,y,w,h = cv2.boundingRect(contours[i])
                rois.append(ROI(float(x),float(y),float(w),float(h),None,method))
        return rois

    def setAllRois(self, value):
         for roi in self.ROIs:
            roi.defect = value

    def compareROIs(self, Rois1, Rois2):
        final_Rois = []
        for roi1 in Rois1:
            roi_unseen = True
            for roi2 in Rois2:
                if roi1 == roi2:
                    if roi1.getObject() is None:
                        if roi2.getObject() is None:
                            raise  AssertionError('method not defined')
                        else:
                            element = roi2.getObject()
                    else:
                        element = roi1.getObject()
                    # print (element)    
                    final_Rois.append(ROI(roi1.x,roi1.y,roi1.w,roi1.h,max(roi1.defect,roi2.defect),element))
                    Rois2.remove(roi2)
                    roi_unseen = False
            if roi_unseen:
                final_Rois.append(roi1)                    
        return final_Rois

