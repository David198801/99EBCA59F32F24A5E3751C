import os

path = r"G:\f\Collections2\音乐\music\CD"
flacPath = r'G:\f\Collections2\音乐\music\flac'

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
                print('[对不上flac文件]' + flac)
        if m2:
            print()
            m2 = False