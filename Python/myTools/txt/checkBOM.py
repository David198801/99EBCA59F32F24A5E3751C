import os,codecs

path = r"D:\music\CD"

def existBOM(file_name):
    file_obj = open(file_name,'br')
    code = file_obj.read(3)
    file_obj.close()
    if code == codecs.BOM_UTF8:#判断是否包含EF BB BF
        return  True
    return False
    
for root,dirs,files in os.walk(path):
    for f in files:
        if f.split('.')[-1] == 'txt':
            fPath = os.path.join(root,f)
            if not existBOM(fPath):
                print(fPath)