import os

path = r"D:\BaiduNetdiskDownload\哆啦A梦+2020.10.11"

outPath = r"D:\linshi\record\哆啦A梦"
if not os.path.exists(outPath):
    os.makedirs(outPath)

l = os.listdir(path)

for i in l:
    txtPath = os.path.join(outPath,i+".txt")
    with open(txtPath,"w",encoding="utf8") as txt:
        for root,dirs,files in os.walk(os.path.join(path,i)):
            for f in files:
                filePath = os.path.join(root,f)
                size = str(os.path.getsize(filePath) // (1024*1024)) + "MB"
                txt.write(filePath)
                print(filePath)
                txt.write("\n")
                txt.write(size)
                txt.write("\n")
                
input("done")