from header import *

dir = "D:/paddy/MOD09A1/" + year + "/" + "mask/"
checkDir(dir)
dirwin = dir.replace("/","\\")
bat = '''d:\ncd {0}\n'''.format(dirwin) + \
'''set MRT_DATA_DIR=e:\\MTR\\data\n''' \
'''set /a DAY=2017001\n''' \
'''set /a DEADLINE=2017365\n''' \
''':start\n''' \
'''if %DAY% leq %DEADLINE% (goto ORDER) else pause\n''' \
''':ORDER\n''' \
'''if exist meta.%DAY%.h27v05.hdf (\n''' \
'''dir meta.%DAY%.*.hdf /a/b/s > MOSAICINPUT.TXT\n''' \
'''E:\\MTR\\bin\\mrtmosaic.exe -i MOSAICINPUT.TXT -s "1" -o  maskMosaic_%DAY%.hdf)\n''' \
'''set /a DAY= %DAY% + 1\n''' \
'''goto start'''.replace("2017",year)


filePath = dir + "mosaicMask.bat"
with open(filePath,"w") as file:
    file.write(bat)

os.system("start " + filePath)