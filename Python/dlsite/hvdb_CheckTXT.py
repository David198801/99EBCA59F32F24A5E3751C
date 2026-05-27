txtPath = 'D:\linshi\hvdb\output.txt'
outPath = 'D:\linshi\hvdb\check.txt'
txtList = []
with open(txtPath,'r',encoding='utf-8-sig') as txt:
    txtList = [x.replace('\n','') for x in txt.readlines()]
    
emptyList = []
commaList = []
for i in txtList:
    if '☯☯☯☯☯☯' in i:
        emptyList.append(i)
    if i.count('☯')>6:
        commaList.append(i)
        


with open(outPath,'w',encoding='utf-8-sig') as txt:
    txt.write('空行\n')
    for i in emptyList:
        txt.write(i+'\n')
        
    txt.write('\n\n\n\n\n')
    
    txt.write('多逗号\n')
    for i in commaList:
        txt.write(i+'\n')