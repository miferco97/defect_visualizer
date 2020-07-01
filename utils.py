import cv2, os
import numpy as np

DISK_MASK_INDEX = 1
INTERDISK_MASK_INDEX = 2

def parseDefectFromBinaryArray(array_defect):
    defect_names = []
    defect_numbers = []
    if array_defect[0]:
        defect_names.append('Rusted Insulator')
        defect_numbers.append(1)
    if array_defect[1]:
        defect_names.append('Broken Insulator Glass')
        defect_numbers.append(2)
    
    if array_defect[2]:
        defect_names.append('Polluted Insulator')
        defect_numbers.append(3)

    if array_defect[3]:
        defect_names.append('Flashover Insulator')
        defect_numbers.append(4)

    if array_defect[4]:
        defect_names.append('Rusted Tower Structure')
        defect_numbers.append(5)

    if array_defect[5]:
        defect_names.append('Bent Tower Bars')
        defect_numbers.append(6)


    return defect_names, defect_numbers
    


def getMaskedImage(image, mask, mask_type, return_mask_only = False):
    
    if mask_type == 'None':
        return image

    mask_ = np.zeros(mask.shape)
    for i in range(3):
        if mask_type == 'disk':
            mask_[:,:,i] = mask[:,:,DISK_MASK_INDEX]/255.0
        if mask_type == 'interdisk':
            mask_[:,:,i] = mask[:,:,INTERDISK_MASK_INDEX]/255.0
        if mask_type == 'both':
            mask_[:,:,i] = mask[:,:,DISK_MASK_INDEX]/255.0 + mask[:,:,INTERDISK_MASK_INDEX]/255.0

    if return_mask_only:
        return mask_

    result = image * mask_.astype(np.uint8)
    return result

def drawDefectNames(image, info ,defect_index):    
    for i,name in enumerate(info['defect_names']):
        size = 1
        if i == defect_index:
            size = 2
        r,g,b = getColorFromDefect(info['defect_numbers'][i])
        result = cv2.putText(image,name, #text
                                (20,(i+1)*30), #position at which writing has to start
                                cv2.FONT_HERSHEY_SIMPLEX, #font family
                                0.6, #font size
                                (r, g, b, 255), #font color
                                size ) #font stroke
    return image
        


def getColorFromDefect(defect):
    if defect == 0:
        color = (255,255,255)
    elif defect == 1:
        color = (255,  0, 255)
    elif defect == 2:
        color = (0  ,255,255)
    elif defect == 3:
        color = (255,200,60)
    elif defect == 4:
        color = (125,125,255)
    elif defect == 5:
        color = (125,255,125)
    elif defect == 5:
        color = (255,125,125)
    else:
        color = (125,125,125)
        
    return color 

def getAppropiateMask(defect_list):
    if not defect_list or (len(defect_list) == 1 and defect_list[0] == 0):
        return 'None' 
    if 5 in defect_list or 6 in defect_list:
        return 'None'
    if not 2 in defect_list and not 3 in defect_list:
        return 'interdisk'
    if not 1 in defect_list and not 4 in defect_list:
        return 'disk'
    
    return 'both'