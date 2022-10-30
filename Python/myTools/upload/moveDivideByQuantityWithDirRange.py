import os
import shutil

path = r"D:\music\2577"

limit = 50
        
l = sorted(os.listdir(path))

fileNum = len(l)
fill = len(str(fileNum))
if fileNum>limit:
  start = 0
  end = limit
  
  dirNum = 0
  
  if fileNum % limit == 0:
    dirNumEnd = fileNum / limit
  else:
    dirNumEnd = fileNum // limit + 1
    
  while True:
    dirPath = os.path.join(path,str(dirNum*limit+1).zfill(fill)+'-'+str(dirNum*limit+limit).zfill(fill))
    if dirNum + 1 == dirNumEnd:
        dirPath = os.path.join(path,str(dirNum*limit+1).zfill(fill)+'-'+str(fileNum).zfill(fill))
    print(dirPath)
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