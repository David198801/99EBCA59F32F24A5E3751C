#coding:utf-8
import requests
from bs4 import BeautifulSoup
import time
import traceback

baseUrl = "https://www.dlsite.com/maniax/work/=/product_id/{0}.html"
with open(r"D:\linshi2\dlsite_all.txt", "r") as txt:
    rjList = [x.replace("\n", "") for x in txt.readlines()]

outPath = "D:\linshi2\dlsite更新" + str(time.time()).split(".")[0]  +".txt"
outFile = open(outPath, "w", encoding="utf-8-sig")
#outFile.write("RJ号,作品容量,发售日期,最终更新日,更新内容\n")

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5",
    "cache-control": "max-age=0",
    # "cookie":"dlsite_dozen=0; uniqid=3j34j2hkp9; adultchecked=1; _ga=GA1.2.263111392.1575779454; _gaid=263111392.1575779454; _d3date=2019-12-08T043056.843Z; _d3landing=1; adr_id=zCQgeesqV8TaXahgQUawgLnlkiMdn1Ih3iTHiZwyBMFPkhQn; _td=8b749f3f-3101-4041-80ab-445b3d3c5d69; session_state=bd8dfc450b587aece1f77eac41328b01e5407f512116d83a2004ee249b804a58.2emoxea5y328k84cook4k4440; loginchecked=1; DL_STAR_ID=6; utm_c=sns_link; locale=zh-cn; __DLsite_SID=hum7arg8bpbv214jf80qam9asl; DL_SITE_DOMAIN=maniax; DL_PRODUCT_LOG=%2CRJ294105%2CRJ292031%2CRJ291298%2CRJ295582%2CRJ277492.htmlRJ262175%2CRJ194353%2CRJ244855%2CRJ163690%2CRJ175899%2CRJ219051%2CRJ245512%2CRJ247761%2CRJ177905%2CRJ224695%2CRJ227798%2CRJ239939%2CRJ239238%2CRJ233647%2CRJ269164%2CRJ290963%2CRJ083355%2CRJ288853%2CRJ223323%2CRJ185915%2CRJ255109%2CRJ255618%2CRJ269057%2CRJ196062%2CRJ231718%2CRJ220732%2CRJ284644%2CRJ207679%2CRJ282003%2CRJ073920%2CRJ278396%2CRJ147133%2CRJ229226%2CRJ285826%2CVJ007373%2CRJ201848%2CRJ244621%2CRJ226737%2CRJ212704%2CRJ218604%2CRJ149609%2CRJ132683%2CRJ116720%2CRJ262563%2CRJ266712%2CRJ117823",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

startRJ = ""
def getRjListNum(startRJ):
    if startRJ:
        for i in range(len(rjList)):
            if startRJ==rjList[i]:
                return i
    else:
        return 0
rjListNum = getRjListNum(startRJ)
def main():
    counterALL = len(rjList) - rjListNum
    counter = 1
    for rjCode in rjList[rjListNum:]:
        outFile.write(rjCode + ",")

        url = baseUrl.format(rjCode)
        print('[' + str(counter) + '/' + str(counterALL) + ']', url)
        counter += 1

        while True:
            try:
                r = requests.get(url, headers=headers, timeout=10)
                #time.sleep(5)
                break
            except Exception as e:
                print(e)
                continue

        soup = BeautifulSoup(r.text, features="lxml")

        sizethLableList = soup.find_all(name='th', string='文件容量')
        size = sizethLableList[0].parent.td.string.replace("\n", "").replace("合计\xa0", '')
        outFile.write(size + ",")

        sellDateLableList = soup.find_all(name='th', string='贩卖日')
        sellDate = sellDateLableList[0].parent.td.string
        outFile.write(sellDate)

        upDateLableList = soup.find_all(name='th', string='最终更新日')
        if upDateLableList:
            upDate = upDateLableList[0].parent.td.text.replace("版本更新情报", "")
            outFile.write(',' + upDate)

            updateInfoDivLableList = soup.find_all(name='div', class_='work_article version_up')
            if updateInfoDivLableList:    
                updateInfoLableList = updateInfoDivLableList[0].ul.find_all('li')
                for updateInfoLable in updateInfoLableList:
                    dlLable = updateInfoLable.dl
                    updateDate = dlLable.dt.string
                    ddLableList = dlLable.find_all('dd')
                    updateTypeSpanLabelList = ddLableList[0].find_all('span')
                    updateType = ''
                    for updateTypeSpanLabel in updateTypeSpanLabelList:
                        updateTypeN = updateTypeSpanLabel.text.replace("\n",'').replace("\r",'')
                        updateType += '【' + updateTypeN + '】'
                    if len(ddLableList) > 1:
                        updateDetail = ddLableList[1].text.replace("\n",'').replace("\r",'')
                        updateInfo = updateDate + updateType + ':' + updateDetail
                    else:
                        updateInfo = updateDate +  updateType
                    outFile.write(',' + updateInfo)

        else:
            upDate = ''

        outFile.write("\n")

    outFile.close()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()  
    except KeyboardInterrupt:
        pass
    finally:
        outFile.close()
