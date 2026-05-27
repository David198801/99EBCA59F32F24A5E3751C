import chardet
import os

p = r"D:\old\苏州\升级0831\2.发版sql"

out = open("out.txt","w",encoding="utf8")

for root,dirs,files in os.walk(p):
    for f in files:
        file_path = os.path.join(root,f)
        if f.lower().endswith(".sql") or f.lower().endswith(".txt"):#os.path.getsize(filePathI)==0
            print(file_path)
            with open(file_path,"rb") as txt:
                result = chardet.detect(txt.read(1024 * 1024))
                if (not result["encoding"]) or (result["confidence"]<0.99):
                    out.write(str(result) + "   "+file_path+"\n")
                    out.flush()
                    
            
out.close()