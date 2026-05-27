from header import *

dir = "D:/paddy/MOD09A1/" + year + "/"
checkDir(dir)
dirwin = dir.replace("/","\\")
bat = '''d:\ncd {0}\n'''.format(dirwin) + \
'''set MRT_DATA_DIR=e:\\MTR\\data\n''' \
'''set /a DAY=2017001\n''' \
'''set /a DEADLINE=2017365\n''' \
'''set name=MYD09A1\n''' \
''':start\n''' \
'''if %DAY% leq %DEADLINE% (goto ORDER) else pause\n''' \
''':ORDER\n''' \
'''if exist %name%.A%DAY%.h27v05*.hdf (\n''' \
'''dir %name%.A%DAY%.*.hdf /a/b/s > MOSAICINPUT.TXT\n''' \
'''E:\\MTR\\bin\\mrtmosaic.exe -i MOSAICINPUT.TXT -s "1 1 1 0 0 1 0 0 0 0 0 0 0" -o  %name%_%DAY%.hdf)\n''' \
'''set /a DAY= %DAY% + 1\n''' \
'''goto start'''.replace("2017",year)

filePath = dir + "mosaic09A1.bat"
with open(filePath,"w") as file:
    file.write(bat)

os.system("start " + filePath)