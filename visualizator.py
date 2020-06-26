import numpy as np
import cv2, os, pdb, csv 

BASE_PATH = 'Dataset/data_test/'
CSV_FILENAME = 'labels_doc.csv'

class DefectDataset():
    def __init__(self, path, mask_type):
        if mask_type == 'disk' or mask_type == 'interdisk' or mask_type == 'both' :
            self.mask_type = mask_type
        else:
            raise AssertionError("This mask type is not allowed")
        
        self.path = path
        self.image_path = path + 'images/'
        self.labels_path = path + 'labels/'

        self.images = sorted(os.listdir(self.image_path))
        self.masks  = sorted(os.listdir(self.labels_path))

        if (len(self.images) != len(self.masks)):
            raise AssertionError(" number of images must be equal to number of labels")
        self.length = len(self.images)
        self.defects = self.readDefects(CSV_FILENAME)

    def __getitem__(self,i):
        defect_row = self.defects[i]

        # print(self.images[i], defect_row['filename'])
        if defect_row['filename'] != self.images[i]:
            raise AssertionError('Both filenames must be equal')
    
        image = cv2.imread(self.image_path+self.images[i])
        mask  = cv2.imread(self.labels_path+self.masks[i])
        mask_ = np.zeros(mask.shape)
    
        for i in range(3):
            if self.mask_type == 'disk':
                mask_[:,:,i] = mask[:,:,1]/255.0
            if self.mask_type == 'interdisk':
                mask_[:,:,i] = mask[:,:,2]/255.0
            if self.mask_type == 'both':
                mask_[:,:,i] = mask[:,:,1]/255.0 + mask[:,:,2]/255.0
                
        result = image * mask_.astype(np.uint8)

        names = self.parseDefect(defect_row['defects']) 
        for i,name in enumerate(names):
            result = cv2.putText(result,name, #text
                                    (20,(i+1)*30), #position at which writing has to start
                                    cv2.FONT_HERSHEY_SIMPLEX, #font family
                                    1, #font size
                                    (209, 80, 0, 255), #font color
                                    2) #font stroke
                                
        return result

    def readDefects(self, filename):
        defects = []
        with open(self.path + filename,mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for i,row in enumerate(csv_reader):
                defect = {'index' : i  , 'filename': row[0] , 'defects': [int(i) for i in row[1:]]}
                defects.append(defect)
        return defects

    def parseDefect(self, array_defect):
        defect_names = []
        # print(array_defect)
        if array_defect[0]:
            defect_names.append('Rusted Insulator')
        if array_defect[1]:
            defect_names.append('Broken Insulator Glass')
        if array_defect[2]:
            defect_names.append('Polluted Insulator')
        if array_defect[3]:
            defect_names.append('Flashover Insulator')
        if array_defect[4]:
            defect_names.append('Rusted Tower Structure')
        if array_defect[5]:
            defect_names.append('Bent Tower Bars')

        return defect_names


    def __len__(self): 
        return self.length


def main():
    dataset = DefectDataset(BASE_PATH, 'both')
    defects = dataset.readDefects('labels_doc.csv')
    
    for i in dataset:
        cv2.imshow('image',i)
        c = cv2.waitKey()
        if c == 27:
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()