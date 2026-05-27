import arcpy
from arcpy.sa import *
from header import *
arcpy.env.overwriteOutput = True

inPath = "D:/paddy/" + year + "/evi/"
outPath = "D:/paddy/" + year + "/"

newOutPath = "D:/paddy/" + year + "/lgeTrans/"
checkDir(newOutPath)

arcpy.env.workspace = inPath

fileList = os.listdir(inPath)

for file1 in fileList:
    if file1[-3:].isdigit():
        for transDay in range(trans[0],trans[1]+1):
            if (year + str(transDay).zfill(3) in file1):
                transP40List = range(transDay, transDay + 40 + 1)
                transCycleList = range(transDay, transDay + 90 + 1)
                ras40 = ""
                rasCycle = ""
                for file in fileList:
                    if file[-3:].isdigit():
                        for day in transP40List:
                            if (year + str(day).zfill(3) in file):
                                # if (year + str(day).zfill(3) in file) and (day not in deleteDay):
                                ras40 += (file + ";")
                        for dayC in transCycleList:
                            if (year + str(dayC).zfill(3) in file):
                                # if (year + str(dayC).zfill(3) in file) and (dayC not in deleteDay):
                                rasCycle += (file + ";")
                ras40 = ras40[:-1]
                rasCycle = rasCycle[:-1]

                print file1

                saveName = "trans40"
                arcpy.MosaicToNewRaster_management(input_rasters=ras40,
                                                   output_location=outPath,
                                                   raster_dataset_name_with_extension=saveName,
                                                   pixel_type="32_BIT_FLOAT",
                                                   number_of_bands=1,
                                                   mosaic_method="MAXIMUM")
                print ras40

                saveName = "transCycle"
                arcpy.MosaicToNewRaster_management(input_rasters=rasCycle,
                                                   output_location=outPath,
                                                   raster_dataset_name_with_extension=saveName,
                                                   pixel_type="32_BIT_FLOAT",
                                                   number_of_bands=1,
                                                   mosaic_method="MAXIMUM")
                print rasCycle

                transRaster = ((arcpy.Raster(outPath + "trans40") * 2) > arcpy.Raster(outPath + "transcycle"))
                lgeRaster = arcpy.Raster("D:/paddy/" + year + "/lswiGTevi/" + "lge_" + file1[-7:])
                outRaster = (transRaster == 1) & (lgeRaster == 1)
                savePath = newOutPath + "lget_" + file1[-7:]
                outRaster.save(savePath)
                print savePath