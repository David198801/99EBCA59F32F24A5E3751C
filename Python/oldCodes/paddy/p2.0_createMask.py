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
    cmd = (r'''E:\LDOPE-1.7\bin\create_mask -of=''' + realOutPath +
           ''' -on=1 -off=0 -mask="''' + cmdPath + file + ''',sur_refl_state_500m, 0-1==01"''')
    print cmd
    os.system(cmd)
    # time.sleep(1)

for file in fileList:
    metaPath = cmdPath + file
    maskPath = cmdOutPath + "mask." + file[9:23] + ".hdf"
    metaoutPath = cmdOutPath + "meta." + file[9:23] + ".hdf"
    cmd = r'''E:\LDOPE-1.7\bin\cp_proj_param -ref=''' + metaPath + ''' -of=''' + metaoutPath + " " + maskPath
    print cmd
    os.system(cmd)
    os.remove(maskPath)
    # time.sleep(1)

# for file in fileList:
#     if file[-3:] == "hdf" and "h27v05" in file:
#         file4 = []
#         file4.append(file)
#         file4.append(file.replace("h27v05", "h27v06"))
#         file4.append(file.replace("h27v05", "h28v05"))
#         file4.append(file.replace("h27v05", "h28v06"))
#         for i in file4:
#             metaPath  = cmdPath + i
#             maskPath = cmdOutPath + "mask." + file[9:23] + ".hdf"
#             metaoutPath = cmdOutPath + "meta." + i[5:]
#             cmd = '''cp_proj_param -ref=''' + metaPath + ''' -of=''' + metaoutPath + " " + maskPath
#             print cmd
#             os.system(cmd)
#             # os.remove(inPath + i)
#             time.sleep(1)