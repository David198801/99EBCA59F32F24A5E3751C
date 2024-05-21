import sys
import os

for i in sys.argv[1:]:
  outList = []
  with open(i,"r") as file:
    readList = [x.replace("\n","") for x in file.readlines()]
    l = 0
    for line in readList:
      if line[0]==" ":
        outList[l-1]=outList[l-1]+line[1:]
      else:
        outList.append(line)
        l+=1
        
  outPath = os.path.join(os.path.dirname(i),"out_"+os.path.basename(i))
  with open(outPath,"w") as outFile:
    for i in outList:
      # if len(i) >72:
        # splitList = i.split('",')
        # outFile.write(splitList[0]+'",\n')
        # for j in splitList[1:-1]:
          # outFile.write(' '+j+'",\n')
        # outFile.write(' '+splitList[-1]+'\n')
      # else:
        # outFile.write(i+"\n")
      outFile.write(i+"\n")