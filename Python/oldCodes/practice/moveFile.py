import os
import shutil
path = "D:/air/day_shp1/"
list = os.listdir(path)
a = "HuBei"
b = "JiangSu"
for file in list:
    for i in range(1998, 2018):
        if i % 4 == 1:
            if (a + str(i) in file) or (b + str(i) in file):
                shutil.move(path + file, "D:/air/day_shp2/"+ file)
        if i % 4 == 2:
            if (a + str(i) in file) or (b + str(i) in file):
                shutil.move(path + file, "D:/air/day_shp3/"+ file)
        if i % 4 == 3:
            if (a + str(i) in file) or (b + str(i) in file):
                shutil.move(path + file, "D:/air/day_shp4/"+ file)