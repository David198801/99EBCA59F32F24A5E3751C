# -*-coding:utf-8-*-
import requests
import re
import datetime

mainUrl = 'https://e4ftl01.cr.usgs.gov'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
headersD = {
    'Cookie': 'DATA=Wf1OZpg9BGcAAExtfK4AAAA2',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
while True:
    try:
        print u'正在连接'
        getMain = requests.get(mainUrl, headers=headers)
        print u'连接成功'
        break
    except:
        print u'连接失败'
print u'正在获取内容'
htmlMain = str(getMain.text).splitlines()
# 获取一级目录（传感器及卫星）
dirMainL = []
for thtmlMain in htmlMain:
    mainDirEnd = re.match(r'.+href=\"(.{1,10}\/)\".+', thtmlMain)
    if mainDirEnd:
        dirMainL.append(mainDirEnd.group(1))
# 获取二级目录（数据代号及版本）
dirSensorL = {}
for tdirMainL in dirMainL:
    rpSensor = requests.get(mainUrl + '/' + tdirMainL, headers=headers)
    htmlSensor = str(rpSensor.text).splitlines()
    dirSensorL[tdirMainL] = []
    for thSensor in htmlSensor:
        endDirSensor = re.match(r'.+href=\"(.{1,15}\/)\".+', thSensor)
        if endDirSensor:
            dirSensorL[tdirMainL].append(endDirSensor.group(1))
def checkCode():  # 函数：检查输入的代号及版本是否存在
    for tdirSensorL in dirSensorL:
        for ttdirSensorL in dirSensorL[tdirSensorL]:
            if (dataCode + '.' + dataEdition).upper() in ttdirSensorL:
                return True
def helpPrint():  # 函数：输出支持的代号及版本
    for tdirSensorL in dirSensorL:
        for ttdirSensorL in dirSensorL[tdirSensorL]:
            print ttdirSensorL[:-1]
print u'获取成功'
while True:  # 输入代号和版本或help，错误则循环输入
    dataCode = raw_input(u'请输入数据代号（例：MOD09GA），或输入“help”查看支持的代号及版本\n')
    if dataCode == 'help':
        helpPrint()
        continue
    dataEdition = raw_input(u'请输入数据版本（例：005），或输入“help”查看支持的代号及版本\n')
    if dataCode == 'help':
        helpPrint()
        continue
    if checkCode():
        break
    else:
        print u'查无此数据'
codeChoose = ''
sDirChoose = ''
for tdirSensorL in dirSensorL:
    for ttdirSensorL in dirSensorL[tdirSensorL]:
        if (dataCode + '.' + dataEdition).upper() in ttdirSensorL:
            codeChoose = ttdirSensorL
            sDirChoose = tdirSensorL
print u'正在获取%s'%codeChoose[:-1]
rpDataset = requests.get(mainUrl + '/' + sDirChoose + codeChoose, headers=headers)
print u'获取成功'
htmlDataset = str(rpDataset.text).splitlines()
dirDateL=[]
for thtmlDataset in htmlDataset:
    endDirDataset= re.match(r'.+href=\"([\d\.\/]{11})\".+', thtmlDataset)
    if endDirDataset:
        dirDateL.append(endDirDataset.group(1))
date1S=dirDateL[0][:-1].replace('.','')
date2S=dirDateL[1][:-1].replace('.','')
dateES=dirDateL[-1][:-1].replace('.','')
date1I = datetime.date(int(date1S[0:4]),int(date1S[4:6]),int(date1S[6:]))
date2I = datetime.date(int(date2S[0:4]),int(date2S[4:6]),int(date2S[6:]))
dateEI = datetime.date(int(dateES[0:4]),int(dateES[4:6]),int(dateES[6:]))
intervalData=(date2I-date1I).days
def checkDate(cDateS):
    if not (cDateS == 'help' or cDateS == 'all' or cDateS.isdigit()):
        return False
    cDate = datetime.date(int(cDateS[0:4]), int(cDateS[4:6]), int(cDateS[6:]))
    if (cDate-date1I).days >= 0 and (dateEI-cDate).days >= 0:
        return True
while True:
    dateStart = raw_input(u'请输入起始日期（例：20080101），或输入“help”查看数据集日期范围（输入“all”查看完整日期表）\n')
    if dateStart == 'help':
        print u'%s-%s,间隔%d天' % (dirDateL[0][:-1], dirDateL[-1][:-1], intervalData)
        continue
    elif dateStart == 'all':
        for tdirDateL in dirDateL:
            print tdirDateL[:-1]
        continue
    elif not checkDate(dateStart):
        print u'日期超出范围'
        continue
    dateEnd = raw_input(u'请输入结束日期\n')
    if not checkDate(dateEnd):
        print u'日期超出范围'
        continue
    break
