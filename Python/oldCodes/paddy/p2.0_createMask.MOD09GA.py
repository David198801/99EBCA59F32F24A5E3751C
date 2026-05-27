import time
from header import *

data = "MOD09A1"

inPath = "D:/paddy/" + data + "/" + year + "/"
outPath = "D:/paddy/" + data + "/" + year + "/mask/"

cmdPath = inPath.replace("/","\\")
cmdOutPath = outPath.replace("/","\\")

checkDir(outPath)

fileList = os.listdir(inPath)

for i in range(len(fileList))[::-1]:
    if fileList[i][-3:] != "hdf" or len(fileList[i]) < 30:
        del fileList[i]

for file in fileList:
    realOutPath = cmdOutPath + "mask." + file[9:23] + ".hdf"
    cmd = (r'''E:\LDOPE-1.7\bin\unpack_sds_bits -of=''' + realOutPath +
           ''' -sds=QC_500m_1 -bit=0-1 -meta ''' + cmdPath + file)
    print cmd
    os.system(cmd)

for file in fileList:
    metaPath = cmdPath + file
    maskPath = cmdOutPath + "mask." + file[9:23] + ".hdf"
    metaoutPath = cmdOutPath + "meta." + file[9:23] + ".hdf"
    cmd = r'''E:\LDOPE-1.7\bin\cp_proj_param -ref=''' + metaPath + ''' -of=''' + metaoutPath + " " + maskPath
    print cmd
    os.system(cmd)
    os.remove(maskPath)
