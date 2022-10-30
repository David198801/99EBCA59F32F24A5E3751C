

with open('a.txt','r',encoding='utf-8-sig') as txt:
   l = [x.replace('\n','') for x in txt.readlines()]
   
for i in l:
    print(i)
    r = ''
    try:
        with open(i,'r',encoding='ascii') as txt:
            r = txt.read()
    except UnicodeDecodeError:
        with open(i,'r',encoding='gbk') as txt:
            r = txt.read()
    with open(i,'w',encoding='utf-8-sig') as txt:
            txt.write(r)