import os

path = r"e:\CD_2020.09.01"
flacPath = 'd:/music/flac'

for i in os.listdir(path):
    albumPath = os.path.join(path,i)
    txtPath = os.path.join(albumPath,'music.txt')
    if not os.path.exists(txtPath):
        print('[无txt文件]\n' + albumPath + '\n')
    else:
        with open(txtPath,'r',encoding='utf-8-sig') as txt:
            flacList = [x.replace('\n','') for x in txt.readlines()]
            flacList = [flacPath + x for x in flacList]
        m = True
        m2 = False
        for flac in flacList:
            if not os.path.exists(flac):
                if m:
                    print(txtPath)
                    m = False
                    m2 = True
                print('[对不上flac文件]\n' + flac)
        if m2:
            print()
            m2 = False