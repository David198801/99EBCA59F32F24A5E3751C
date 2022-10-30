import os

path = r"D:\BaiduNetdiskDownload\秋野かえで 音声 动画 合集 pw hmoe.moe"
fakeExt = "txt"

def checkFakeExt(fs):
    for i in fs:
        i = i.lower()
        if i == "rar" or i == "7z" or i == "zip" or "part" in i:
            return True


for root, dirs, files in os.walk(path):
    for f in files:
        if f[-3:].lower()==fakeExt:
            fs = f.split(".")
            if checkFakeExt(fs):
                old = os.path.join(root,f)
                new = old.replace("."+fs[-1],"")
                if new != old:
                    os.rename(old, new)
                    print(new)
