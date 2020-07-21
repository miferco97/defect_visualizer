import  cv2,pdb,os
from dataset_generator import * 
from tqdm import tqdm

DISK_PATH = BASE_PATH + '/cropped/disk/'
INTERDISK_PATH  = BASE_PATH + '/cropped/interdisk/'

def checkFolders():
    os.makedirs(DISK_PATH,exist_ok=True)
    os.makedirs(INTERDISK_PATH,exist_ok=True)

def findDestinyPath(label):
    
    if label[-1] in [-1,3]:
        return DISK_PATH
    elif label[-1] in [-2,1,4]:
        return INTERDISK_PATH
    else:
        return None

def cutImage(image, label):
    out = image.copy()
    out = out[label[1]:label[1]+label[3],label[0]:label[0]+label[2],:]
    return out

def LoadData(filename):
    file_path = None
    image_path = None

    if filename.endswith('.txt'):
        file_path = filename
        image_path = filename.replace('.txt','.png')
    
    elif filename.endswith('.png'):              
        image_path = filename
        file_path = filename.replace('.png','.txt')

    image = cv2.imread(image_path)
    labels = readTxt(file_path)
    if NORMALIZED_HEIGTH:
        old_labels = labels.copy()
        labels.clear()
        image_scale = NORMALIZED_HEIGTH / image.shape[0]
        for line in old_labels:
            new_line = [int(line[i]/image_scale) for i in range(4)]
            new_line.append(line[4])
            labels.append(new_line)
        final_size = (int(image.shape[1]*image_scale),int(image.shape[0]*image_scale))
    

    return image, labels
    
def readTxt(filename):
    lines = None
    out = []
    if os.path.exists(filename):    
        with open(filename,'r') as f:
            lines = f.readlines()
        for line in lines:
            data = line.lstrip().rstrip().split(' ')
            if int(data[-1]) != 0:
                out.append(data)
            for i,_ in enumerate(data):
                data[i] = int(float(data[i]))
    return out

def cropImages(path = BASE_PATH):
    files = []
    image_path = BASE_PATH + '/images/'
    for element in sorted(os.listdir(image_path)):
        if element.endswith('.txt'):
            files.append(element)
    for filename in tqdm(files):
        print(image_path + filename)
        image,labels = LoadData(image_path + filename)
        for i,label in enumerate(labels):
            cropped = cutImage(image,label)
            folder = findDestinyPath(label)
            if folder is None or cropped.shape[0]*cropped.shape[1] < 60*60:
                continue
            name = filename.split('.')[0] + '_' +str(i).zfill(2) 
            cv2.imwrite(folder+name+'.png',cropped)
            with open(folder+name+'.txt','w') as file:
                if label[-1]  < 0:
                    file_line = str(0)
                else:
                    file_line = str(label[-1])
                file.write(file_line)

if __name__ == "__main__":
    checkFolders()
    cropImages()