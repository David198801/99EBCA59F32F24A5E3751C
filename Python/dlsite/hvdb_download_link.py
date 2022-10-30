import requests
import time
from bs4 import BeautifulSoup
import re


headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5",
"Cache-Control":"max-age=0",
"Cookie":"__cfduid=de9062354df09c1cb3cba97d2856c63831601520698; __RequestVerificationToken=nC8BoxCd3Z9H0CoWiPVDw3OIPHWsmA5zRvmCWZ1pJzzWOLZcobVrFhGHJUnU57taMrgMTiov-LO_qDyHT-PoKxEbRvn65Qhzc3utNhNZxvs1; .AspNet.ApplicationCookie=vW_aqEEDY8JzRl5l0Fu3BHjwabGwrsSY55iPG7Z_VNfcyu2pioX4sa8NZ_9AFvH2yz22kh-hOyMgtrbaeUO0T2VmpnlD5bBJDUjcVHNu7XNxowER-ITzORJ4D3mgBv3fAOCU9J2n5cJuibbMX4Z6SCiYboc2q3lH1iouif23Wu1vY9wCHbhkFEJ3ms36WHhfvOXtgrd8Pll1Yn4XkM6Qx_ylYTI5OWc1lVPN7p6hu1fi8WvboFfJO074uK-1jPjL3nnUGNeqLxoOn8URPtTcnJ70BDa9xpEGuxkab90n5BfSl8N7rbmU9DAYaW9c86fjx10_M5tXnkTRa_lFEblRcbT4sFfrd8XKZG13pJsOmGpgYg8NFG65ef8qsWpImlT-UZj9-a6JNECeL2B8QbKsrJIcewEBkTUBkDCI_weowBRp1TFdHVX2NyVarfIpFdyc_Q5Wvtw0cUGcknHEHxmCwSCagbNeMJ1FP0Z2xRmiaLgRZeQ38QWYEAz0uM4fFwC45F5U9u_3VWToqJx6d9R48Q",
"Host":"hvdb.me",
"Proxy-Connection":"keep-alive",
"Referer":"hhttp://hvdb.me/Dashboard/AllWorks/",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}


txtPath = r"D:\linshi\hvdb_dy.txt"

outTxtPath = r"D:\linshi\hvdb_download_link_" + str(time.time()).split(".")[0] + '.txt'
outTxt = open(outTxtPath,'w',encoding='utf-8-sig')
#outTxt.write('RJ号☯Download1☯Password1☯Download2☯Password2☯Download3☯Password3\n')


rjList = []
with open(txtPath,'r') as txt:
    rjList = [x.replace('\n','') for x in txt.readlines()]
    
    
    
url_base = r"http://hvdb.me/Dashboard/WorkDetails/"

allNumStr = str(len(rjList))
counter = 0

for rjCode in rjList:
    time.sleep(1)
    counter += 1
    print('[' + str(counter) + '/' + allNumStr + ']' + rjCode)
    rjNumber = rjCode.replace('RJ','')
    
    while rjNumber[0] == '0':
        rjNumber = rjNumber[1:]



    outTxt.write(rjCode)
    outTxt.write('☯')

    downloadLinkList = []
    url = url_base + rjNumber
    while True:
        try:
            page = requests.get(url, headers=headers, timeout=10)
            break
        except Exception as e:
            print(e)
            continue
    soup = BeautifulSoup(page.text, features="lxml")
    buttonLabelList = soup.find_all(name='button',class_="btn btn-default downloadLink")
    
    downloadLinkList = ['']*6
    for buttonLabel in buttonLabelList:
        downloadLink = buttonLabel['data-clipboard-text']
        buttonText = buttonLabel.text
        if 'Download2' in buttonText:
            downloadLinkList[2] = downloadLink
        elif 'Download3' in buttonText:
            downloadLinkList[4] = downloadLink
        else:
            downloadLinkList[0] = downloadLink
            
    passwordLabelList = []
    visibleDivList = soup.find_all('div',class_='form-group infoLabel')
    for v in visibleDivList:
        passwordLabelList += v.find_all('label',{'for':re.compile(r"Password\d{0,1}")})
    for passwordLabel in passwordLabelList:
        password = passwordLabel.parent.div.text.replace('\r','').replace('\n','')
        while password[0]==' ':
            password = password[1:]
        while password[-1] == ' ':
            password = password[:-1]
        
        
        passwordLabelForAttribute = passwordLabel['for']
        if 'Password2' == passwordLabelForAttribute:
            downloadLinkList[3] = password
        elif 'Password3' == passwordLabelForAttribute:
            downloadLinkList[5] = password
        else:
            downloadLinkList[1] = password
    
    writeStr = ''
    for d in downloadLinkList:
        writeStr += d
        writeStr += '☯'
    outTxt.write(writeStr[:-1])
    
    outTxt.write('\n')
    outTxt.flush()

outTxt.close()

    