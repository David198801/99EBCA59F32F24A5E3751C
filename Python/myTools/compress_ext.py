import os
import subprocess

path = r"D:\Soft"
ext = ["iso","mds","mdf","nrg","ccd","bin","mdx"]
ext = ["iso"]
for root,dirs,files in os.walk(path):
    for f in files:
        if f.split(".")[-1].lower() in ext:
            filePath = os.path.join(root,f)
            cmd = r'''D:\Program Files\WinRAR\rar.exe a ''' + '\"' + filePath + '.rar\" ' + '\"' + filePath + '\" '
            cmd += "-ep1 -rr5 -v2048m -df"
            print(cmd)
            ps = subprocess.Popen(cmd)
            ps.wait()
            