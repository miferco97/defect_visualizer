import os,shutil
from  tqdm import tqdm

ORIGIN_PATH_1 = './Dataset/test1/'
ORIGIN_PATH_2 = './Dataset/test2/'
 
DESTINY_FOLDER_1 = './Dataset/destiny1/'
DESTINY_FOLDER_2 = './Dataset/destiny2/'


def main():
    files_1 = os.listdir(ORIGIN_PATH_1)
    files_2 = os.listdir(ORIGIN_PATH_2)
    for f in tqdm(files_1):
        if f in files_2:
            shutil.copy2(ORIGIN_PATH_1+f,DESTINY_FOLDER_1+f)
        else:
            shutil.copy2(ORIGIN_PATH_1+f,DESTINY_FOLDER_2+f)

if __name__ == "__main__":
    main()
