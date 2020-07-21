import numpy as np
import cv2, os, pdb, csv
from dataset_generator import ImagesDataset,BASE_PATH
from cycleLists import *

DEFECT_LIST = [0,2]
class Labeler():
    actual_filename = ''
    actual_image = None
    actual_defects  = CycleList(DEFECT_LIST)
    actual_info = None
    
    index = None
    defect_index = None


    def __init__(self, window_name = 'labeler'):
        self.window_name = window_name
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name,self.clickCallback)

    def loadLabel(self,filename):
        self.label_filename = filename.replace('.png', '.txt')
        if os.path.exists(self.label_filename):
            with open(self.label_filename,'r') as f:
                line = f.read()
                line = line.rstrip().lstrip().split(' ')
                index = DEFECT_LIST.index(int(line[-1]))
                self.actual_defects.setInternalIndex(index)
        else:
            index = DEFECT_LIST.index(0)
            self.actual_defects.setInternalIndex(index)
        

                

    def updateImage (self, image):
        r,g,b = (255,0,10)
        size = 3
        result = cv2.putText(image.copy(),'Defect : ' + str(self.actual_defects.get()), #text
                                (20,(0+1)*30), #position at which writing has to start
                                cv2.FONT_HERSHEY_SIMPLEX, #font family
                                1, #font size
                                (b, g, r, 255), #font color
                                size ) #font stroke

        cv2.imshow(self.window_name, result)
          
    def saveImageData(self):
        with open(self.label_filename,'w') as f:
                line = "%4.3f %4.3f %4.3f %4.3f %d\n" %(0,0,0,0,self.actual_defects.get())
                f.write(line)

    def run(self,dataset):
        end = False
        self.index = CycleIndexes(len(dataset))
        change_image = False
        while not end:
            image, filename = dataset[self.index.get()]
            print('file: ', filename)
            self.loadLabel(filename)
            self.updateImage(image)
            
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
            
                elif c == ord('1') or c == ord('2'):
                    self.actual_defects.next()
                    self.updateImage(image)
                elif c == -1:
                    pass                    
                else:
                    self.index.next()
                    change_image = True

            self.saveImageData()
            change_image = False


    def clickCallback(self,event,x,y,flags,param):
        pass
        # if event == cv2.EVENT_LBUTTONDOWN:
        #     self.ROIarray.toggleDefect(x,y,self.actual_defects[self.defect_index.get()])
        #     self.update()
    
def main():
    PATH = 'Dataset/data_broken_insulator/'
    window = Labeler()
    dataset = ImagesDataset(PATH)
    window.run(dataset)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()