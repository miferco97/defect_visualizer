import os
from  tqdm import tqdm

PATH_1 = './Dataset/test1/'
PATH_2 = './Dataset/test2/'
DESTINY_FOLDER = './Dataset/merged_files/'


def merge(files_1,files_2,path1,path2, destiny_path = DESTINY_FOLDER):
    files_1_copy = files_1.copy()
    files_2_copy = files_2.copy()
    
    for f1 in tqdm(files_1_copy):
        lines = []
        with open(path1+f1,'r') as f:
            lines = f.readlines()
        if f1 in files_2_copy:
            with open(path2+f1,'r') as f:
                lines.extend(f.readlines())
            files_2.remove(f1)
        files_1.remove(f1)
        lines = [x.rstrip().lstrip() + '\n' for x in lines if x.rstrip().lstrip()]
        with open(destiny_path+f1,'w') as f:
            f.writelines(lines)
    
    return files_1,files_2


def main():
    files_1 = os.listdir(PATH_1)
    files_1 = [x for x in files_1 if x.endswith('.txt')] 
    files_1 = sorted(files_1)

    files_2 = os.listdir(PATH_2)
    files_2 = [x for x in files_2 if x.endswith('.txt')] 
    files_2 = sorted(files_2)

    merge(files_1,files_2,PATH_1,PATH_2)
    merge(files_2,files_1,PATH_2,PATH_1)

if __name__ == "__main__":
    main()