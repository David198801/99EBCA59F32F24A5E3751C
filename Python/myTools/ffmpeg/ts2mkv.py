import os
import subprocess
import shutil

path = r"H:\f\netbackup\动画\ドラえもん剧场版wowow\1080P 日语原版 全"
ext = ".ts"
outExt = ".mkv"
exParams = ["-bsf:a","aac_adtstoasc"]
# exParams = []

for root,dirs,files in os.walk(path):
    for f in files:
        if f.lower().endswith(ext):
            inPath = os.path.join(root,f)
            inSize = os.path.getsize(inPath)
            outPath = inPath[:-len(ext)] + outExt
            print("=============================================")
            print(outPath)
            cmdList = ["ffmpeg","-y","-i",inPath,"-c","copy","-map","0:a","-map","0:v"]
            cmdList += exParams
            cmdList += [outPath]
            subprocess.run(cmdList)
            if os.path.exists(outPath):
                outSize = os.path.getsize(outPath)
                if outSize > 0.7 * inSize:
                    os.remove(inPath)