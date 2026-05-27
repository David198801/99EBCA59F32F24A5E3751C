import os
import shutil
path = "D:/paddy/"
fileList = os.listdir(path)
for file in fileList:
    if file[:7]=="MOD09A1" and file[-3:]=="hdf":
        outPath = path+"MOD09A1/"+file[9:13]
        shutil.move(path+file,outPath)