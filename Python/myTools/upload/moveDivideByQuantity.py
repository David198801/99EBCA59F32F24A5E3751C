import os
import shutil

path = r"D:\music\2577"

limit = 100
        
l = os.listdir(path)

fileNum = len(l)
    
if fileNum>limit:
  start = 0
  end = limit
  
  dirNum = 0
  
  if fileNum % limit == 0:
    dirNumEnd = fileNum / limit
  else:
    dirNumEnd = fileNum // limit + 1
    
  while True:
    print(dirNum)
    dirPath = os.path.join(path,str(dirNum))
    os.makedirs(dirPath)
    for i in l[start:end]:
      old = os.path.join(path,i)
      new = os.path.join(dirPath,i)
      shutil.move(old,new)
      
    dirNum += 1
    start = end
    end += limit
    if end > fileNum:
      end = fileNum
      
    if dirNum == dirNumEnd:
      break