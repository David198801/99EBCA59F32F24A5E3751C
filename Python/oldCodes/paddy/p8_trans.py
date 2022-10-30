import arcpy
from arcpy.sa import *
from header import *
arcpy.env.overwriteOutput = True

inPath = "D:/paddy/" + year + "/evi/"
outPath = "D:/paddy/" + year + "/"

arcpy.env.workspace = inPath

transP40List = range(trans[0],trans[1]+40+1)
transCycleList = range(trans[0],trans[1]+90+1)
# transP40List = range(121,121+40+1)
# transCycleList = range(121,121+90+1)
# deleteDay = [121,129]

fileList = os.listdir(inPath)

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

print ras40
print rasCycle

saveName = "trans40"
arcpy.MosaicToNewRaster_management(input_rasters=ras40,
                                   output_location=outPath,
                                   raster_dataset_name_with_extension=saveName,
                                   pixel_type="32_BIT_FLOAT",
                                   number_of_bands=1,
                                   mosaic_method="MAXIMUM")
print saveName

saveName = "transCycle"
arcpy.MosaicToNewRaster_management(input_rasters=rasCycle,
                                   output_location=outPath,
                                   raster_dataset_name_with_extension=saveName,
                                   pixel_type="32_BIT_FLOAT",
                                   number_of_bands=1,
                                   mosaic_method="MAXIMUM")
print saveName