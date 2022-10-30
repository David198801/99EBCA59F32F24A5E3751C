import os

path = r"E:\CD_2020.09.01"
c = 'utf-8-sig'

#A替换成B
replaceA = '张韶涵'
replaceB = '張韶涵'

for root,dirs,files in os.walk(path):
    for f in files:
        if f.split('.')[-1] == 'txt':
            fPath = os.path.join(root,f)
            with open(fPath,'r',encoding=c) as txt:
                r = txt.read()

            if replaceA in r:
                r = r.replace(replaceA,replaceB)
                with open(fPath,'w',encoding=c) as txt:
                    txt.write(r)
                print('[done]  ' + fPath)
            #else:
                #print('[ignore]  ' + fPath)