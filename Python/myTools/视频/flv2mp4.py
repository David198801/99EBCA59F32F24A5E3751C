import os
import subprocess

path = r"D:\P\Aria2\Download"

for root,dirs,files in os.walk(path):
    for f in files:
        if f[-3:] == 'flv':
            flvPath = os.path.join(root,f)
            mp4Path = flvPath[:-4] + ".mp4"
            if not os.path.exists(flvPath + ".aria2"):
                cmd = ['ffmpeg','-i',flvPath,'-c','copy',mp4Path]
                subprocess.call(cmd)
                os.remove(flvPath)