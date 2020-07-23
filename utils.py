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
    

def maskProcessing(mask):
    ret2,th2 = cv2.threshold(mask,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    out = th2
    kernel = np.ones((5,5),np.uint8)
    out = cv2.morphologyEx(out, cv2.MORPH_OPEN, kernel)
    out = cv2.morphologyEx(out, cv2.MORPH_OPEN, kernel)
    out = cv2.morphologyEx(out, cv2.MORPH_OPEN, kernel)
    return out.astype(np.float32)


def setMaskOpacity(mask, opacity):
    if opacity == 0 :
        mask = np.ones(mask.shape)
    else:
        opacity = 1 - opacity

    mask = mask/np.max(mask)
    mask *= mask * (1 - opacity)
    mask += opacity
    
    return mask

def getMaskedImage(image, mask, mask_type, return_mask = None, opacity = 1):
    
    
    if mask_type == 'None':
        return image
    
    if return_mask == 'Original':
        return mask.copy() 
    _mask = mask.copy()
    mask_ = np.zeros(mask.shape)
    for i in range(3):
        if mask_type == 'disk' or mask_type == 'both': 
            # mask_[:,:,i] = mask[:,:,DISK_MASK_INDEX]/255.0
            mask_[:,:,i] += maskProcessing(_mask[:,:,DISK_MASK_INDEX])
            
        if mask_type == 'interdisk' or mask_type == 'both' :
            mask_[:,:,i] += maskProcessing(_mask[:,:,INTERDISK_MASK_INDEX])

    # cv2.imshow('mask',mask_)
    if return_mask == 'filtered':
        return mask_
    
    
    result = image * setMaskOpacity(mask_,opacity)
    return result.astype(np.uint8)

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
    elif defect == -1:
        # RGB BGR
        color = (0,165,255)
    elif defect == -2:
        color = (71,99,255)
    else:
        color = (125,125,125)
        
    return color 


def getTextFromDefect(defect):
    if defect == 1:
        text = 'Rusted'
    elif defect == 2:
        text = 'Broken'
    elif defect == 3:
        text = 'Polluted'
    elif defect == 4:
        text = 'Flashover'
    elif defect == 6:
        text = 'Bent'
    else :
        text = ''    
    return text 




def getAppropiateMask(defect_list):

    # if not defect_list or (len(defect_list) == 1 and defect_list[0] == 0):
    #     return 'None' 
    # if 5 in defect_list or 6 in defect_list:
    #     return 'None'
    # if not 2 in defect_list and not 3 in defect_list:
    #     return 'interdisk'
    # if not 1 in defect_list and not 4 in defect_list:
    #     return 'disk'
    
    return 'both'