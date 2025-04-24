with open('dlsite更新1596258625.txt','r',encoding='utf-8-sig') as txt:
    l = [x.replace('\n','') for x in txt.readlines()]
    lineMax = 0
    for i in range(len(l)):
        lineNum = 0
        for j in l[i]:
            if j==',':
                lineNum+=1
        if lineNum>lineMax:
            lineMax = lineNum
            print(lineMax,i+1)
    print(lineMax)