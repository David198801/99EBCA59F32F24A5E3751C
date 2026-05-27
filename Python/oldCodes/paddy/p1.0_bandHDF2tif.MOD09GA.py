from osgeo import gdal
from header import *

data = "MOD09A1"

inPath = "D:/paddy/" + data + "/" + year + "/"
outPath = "D:/paddy/" + data + "/" + year + "/" + "bandTif/"

checkDir(outPath)

fileList = os.listdir(inPath)

for file in fileList:
    if file[-3:] == "hdf" and len(file) < 30:
        inRasHDF = inPath + file
        ds = gdal.Open(inRasHDF)
        for band in range(4):
            inRasBand = ds.GetSubDatasets()[band][0]
            outRasBand = outPath + "b{0}_".format(inRasBand[-3]) + file[-11:-4] + ".tif"
            gdal.Translate(outRasBand, inRasBand)
            print outRasBand