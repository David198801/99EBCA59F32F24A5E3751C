
txtPath = r"D:\linshi2\自用密码合并.txt"

limit = 9000
        
with open(txtPath,"r",encoding="utf8") as txt:
  l = txt.readlines()
  txtLength = len(l)
  start = 0
  end = limit
  fileNum = 0
  if txtLength % limit == 0:
    fileNumEnd = txtLength / limit
  else:
    fileNumEnd = txtLength // limit + 1
  while True:
    filePath = txtPath[:-4] + "devide" + str(fileNum) + txtPath[-4:]
    with open(filePath,"w",encoding="utf_8_sig") as oTxt:
      oTxt.writelines(l[start:end])
    fileNum += 1
    start = end
    end += limit
    if fileNum == fileNumEnd:
      break
