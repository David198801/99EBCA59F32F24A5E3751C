#-*-coding:utf-8-*-
import requests
import re
mainUrl='https://e4ftl01.cr.usgs.gov'
headers = {
    'Cookie': 'CFIWebMonPersistent-57=%7B%22LastAccept%22%3A1506087707238%2C%22LastDecline%22%3Anull%7D; _ga=GA1.2.1980364493.1506086283; DATA=WfvU75g9BGcAADDL6CoAAABp',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
data = {
        'scope': 'uid',
        'app_type': '401',
        'client_id': 'ijpRZvb9qeKCK5ctsn75Tg',
        'response_type': 'code',
        'state': 'aHR0cHM6Ly9lNGZ0bDAxLmNyLnVzZ3MuZ292L01PTEEvTVlEMDlDTUcuMDA1LzIwMDIuMDcuMTYvTVlEMDlDTUcuQTIwMDIxOTcuMDA1LjIwMDcxNjYyMTI5MTMuaGRm'}
while True:
    try:
        print u'正在连接'
        getMain = requests.get(mainUrl, data=data, headers=headers)
        print u'连接成功'
        break
    except:
        print u'连接失败'
print u'正在获取内容'
htmlMain = str(getMain.text).splitlines()
dirMainL=[]
for thtmlMain in htmlMain:
    mainDirEnd = re.match(r'.+href=\"(.{1,10}\/)\">.+', thtmlMain)
    if mainDirEnd:
        dirMainL.append(mainDirEnd.group(1))
dirSensorL=[]
for tdirMainL in dirMainL:
    rpSensor =requests.get(mainUrl+'/'+tdirMainL, data=data, headers=headers)
    htmlSensor=str(rpSensor.text).splitlines()
    for thSensor in htmlSensor:
        endDirSensor=re.match(r'.+href=\"(.{1,15}\/)\">.+', thSensor)
        if endDirSensor:
            dirSensorL.append(endDirSensor.group(1))
def checkCode():
    for tdirSensorL in dirSensorL:
        if (dataCode+'.'+dataEdition).upper() in tdirSensorL:
            return True
while True:
    dataCode = raw_input(u'请输入数据代号（例：MOD09GA），或输入“help”查看支持的代号及版本\n')
    dataEdition = raw_input(u'请输入数据版本号（例：005），或输入“help”查看支持的代号及版本\n')
    if dataCode == 'help' or dataEdition == 'help':
        for tdirSensorL in dirSensorL:
            print tdirSensorL[:-1]
    elif checkCode():
        break
    else:
        print u'查无此数据'
