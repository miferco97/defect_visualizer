import cv2, os
import numpy as np


def parseDefectFromBinaryArray(array_defect):
    defect_names = []
    defect_numbers = []
    # print(array_defect)
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
    mask_ = np.zeros(mask.shape)
    for i in range(3):
        if mask_type == 'disk':
            mask_[:,:,i] = mask[:,:,1]/255.0
        if mask_type == 'interdisk':
            mask_[:,:,i] = mask[:,:,2]/255.0
        if mask_type == 'both':
            mask_[:,:,i] = mask[:,:,1]/255.0 + mask[:,:,2]/255.0

    if return_mask_only:
        return mask_

    result = image * mask_.astype(np.uint8)
    return result

def drawDefectNames(image, info ,defect_index):    
    for i,name in enumerate(info['defect_names']):
        size = 1
        if defect_index == 0:
            pass
        else:
            j = defect_index - 1
            if i == j: 
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
        color = (255,255,0)
    elif defect == 4:
        color = (125,125,255)
    elif defect == 5:
        color = (125,255,125)
    elif defect == 5:
        color = (255,125,125)
    else:
        color = (125,125,125)
        
    return color 
