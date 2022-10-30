import os
import subprocess
import shutil

path = r"F:\shareTest\test\[lenfried][全集]\下限少女"
exePath = r"C:\p\7-Zip\7z.exe"

l = os.listdir(path)

for i in l:
    workPath = os.path.join(path,i)
    if os.path.isdir(workPath):
        outPath = workPath + ".tar"
        print(workPath)
        subprocess.run([exePath,"a","-ttar","-sdel",outPath,workPath])