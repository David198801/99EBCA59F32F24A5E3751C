import os

outPath = r"D:/linshi/l42"
dataPath = r"D:\linshi\新建文件夹 (2)\admin.db.txt"

def makeFile(filePath):
    dirPath = os.path.dirname(filePath)
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    with open(filePath,"w") as txt:
        txt.write("a")
        print(filePath)

def txt2file(dataPath):
    dataList = []
    with open(dataPath,"r",encoding="utf-8") as txt:
        dataList = [x.replace("\n","").split("|") for x in txt.readlines()]
    for i in dataList:
        if i[0] == "0":
            filePath = outPath + i[1] + i[2]
            if len(filePath) < 260:
                makeFile(filePath)

txt2file(dataPath)

'''
baiduPath = r"D:\linshi\百度网盘"
baiduList = os.listdir(baiduPath)
for i in baiduList:
    txtSplit = i.split(".")
    if txtSplit[-1]=="txt":
        txtPath = os.path.join(baiduPath,i)
        txtDir = txtSplit[0]
        txtDirPath = os.path.join(outPath,txtDir).replace("\\","/")
        os.makedirs(txtDirPath)
        
        dataList = []
        with open(txtPath,"r",encoding="utf-8") as txt:
            dataList = [x.replace("\n","").split("|") for x in txt.readlines()]
        for i in dataList:
            if i[0] == "0":
                filePath = txtDirPath + i[1] + i[2]
                if len(filePath) < 260:
                    makeFile(filePath)
                
'''