import os
import shutil

a={"RJ037228":r'''aaaaaaa'''}
path = r"E:\RJ\手动"
l = os.listdir(path)
for i in l:
    rjCode = i[:8]
    for aa in a:
        if rjCode == aa:
            name = a[aa].replace("/",u"／").replace("\\",u"＼").replace("?",u"？").replace("*",u"＊").replace("|",u"｜")\
        .replace(":",u"：").replace("<",u"＜").replace(">",u"＞").replace('''"''',u'''＂''')
            d = aa + " " + name
            old = os.path.join(path,i)
            newD = os.path.join(path,d)
            new = os.path.join(path,d, i)

            if not os.path.exists(newD):
                os.makedirs(newD)
            shutil.move(old,new)
            print(new)
