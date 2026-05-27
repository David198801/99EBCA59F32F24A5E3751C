from osgeo import gdal
from header import *

data = "MOD09A1"
dirName = "mask"

inPath = "D:/paddy/" + data + "/" + year + "/" + dirName + "/"
outPath = "D:/paddy/" + data + "/" + year + "/" + "masktif/"

checkDir(outPath)

fileList = os.listdir(inPath)

for file in fileList:
    if file[-3:] == "hdf" and file[:10] == "maskMosaic":
        inRas = inPath + file
        outRas = outPath + file[:-3] + "tif"
        gdal.Translate(outRas,inRas)
        print outRas
