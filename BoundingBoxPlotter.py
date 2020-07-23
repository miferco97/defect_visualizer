import numpy as np
import cv2, os, pdb, csv
from dataset_generator import ImagesDataset,BASE_PATH
from cycleLists import *
from utils import *
from ROI import ROI
from tqdm import tqdm

LOAD_FOLDER = 'Dataset/ree_test/images/'
DESTINY_FOLDER = 'Dataset/ree_test/BoundingBoxes/'


class BoundingBox(ROI):
    
    def __init__(self,x,y,w,h, defect):
        super().__init__(x,y,w,h,defect,element=None)

    def plotRectangle(self, image ,thickness = 2):
        if self.defect <= 0:
            return image

        color = getColorFromDefect(self.defect)            
     
        text = getTextFromDefect(self.defect)
        if self.defect == 2:

            start_point = (0,0)
            
            letter_font, size  = 1 , 2
            px_w_per_letter,px_h_per_letter = 17,50
            text = 'Broken Insulator glass'

            end_point = (int(len(text) * letter_font * px_w_per_letter), int(letter_font * px_h_per_letter ))
            image = cv2.rectangle(image, start_point , end_point, (0,0,0,0.1), -1)
            
         

            dx, dy = 5 , 0.7
            start_text = int(start_point[0] + dx), int (start_point[1] + dy*px_h_per_letter)

            r,g,b = color
            result = cv2.putText(image,text, #text
                                    start_text, #position at which writing has to start
                                    cv2.FONT_HERSHEY_SIMPLEX, #font family
                                    1, #font size
                                    (r, g, b, 255), #font color
                                    2) #font stroke
        
        else:
            image = super().plotRectangle(image,thickness)
            if not text:
                return image

            start_point = (int(self.x)-thickness//2,int(self.y))
            
            letter_font, size  = 0.8 , 2
            px_w_per_letter,px_h_per_letter = 18,26
            

            end_point = (int(self.x + len(text) * letter_font * px_w_per_letter), int(self.y - letter_font * px_h_per_letter ))
            image = cv2.rectangle(image, start_point , end_point, color, -1)
            r,g,b = 0,0,0
            
            dx, dy = 2,2
            start_text = start_point[0]+dx,start_point[1]-dy
            result = cv2.putText(image,text, #text
                                    start_text, #position at which writing has to start
                                    cv2.FONT_HERSHEY_SIMPLEX, #font family
                                    letter_font, #font size
                                    (r, g, b, 255), #font color
                                    size ) #font stroke
        return image

        

class BBploter():
    
    bounding_boxes = []

    def __init__(self, load_folder, destiny_folder):
        self.load_folder = load_folder
        self.dataset = ImagesDataset(load_folder, normalize = False)
        self.destiny_folder = destiny_folder

    def loadLabel(self,filename):
        
        self.bounding_boxes.clear()

        self.label_filename = filename.replace('.png', '.txt')
        if os.path.exists(self.label_filename):
            with open(self.label_filename,'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.rstrip().lstrip().split(' ')
                    if len(line) >= 5:
                        x,y,w,h,defect = float(line[0]),float(line[1]),float(line[2]),float(line[3]),int(line[4])
                        self.bounding_boxes.append(BoundingBox(x,y,w,h,defect))


    def updateImage (self, image):
        for BB in self.bounding_boxes:
            BB.plotRectangle(image)
        # cv2.imshow('test',image)

    def run(self):
        for image, filename in tqdm(self.dataset):
            self.loadLabel(filename)
            self.updateImage(image)
            name = filename.split('/')[-1]
            cv2.imwrite(self.destiny_folder+name,image)
            # c = cv2.waitKey()
            # if c == 27:
            #     break
            
    
    def showDestinyImages(self):
        pass
       
def main():
    plotter = BBploter(LOAD_FOLDER,DESTINY_FOLDER)
    plotter.run()
if __name__ == "__main__":
    main()