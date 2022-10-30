#coding:utf8
import re
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
# proxies = {
#   "http": "http://127.0.0.1:1088",
#   "https": "http://127.0.0.1:1088",
# }

#wordList = [u"体験"]排除体验版，未写完

# name = u"伊ヶ崎綾香"
# name = u"秋野かえで"
# name = u"御崎ひより"
# name = u"藤堂れんげ"
# name = u"餅よもぎ"
# name = "一之瀬りと"
# name = u"御崎ひより"
# name = u"伊ヶ崎綾香"
# name = u"柚木朱莉"
# name = u"箱河ノア"
# name = u"天知遥"
# name = u"浅見ゆい"
name = "小春日より"
# name = "猫乃緒みみ"


mode = 2 #0 声优（不全）  1 固定链接 2 关键词

filename = ""

urlNAME = u"https://www.dlsite.com/maniax/fsr/=/language/jp/sex_category%5B0%5D/male/" \
              u"work_category%5B0%5D/doujin/order%5B0%5D/dl_d/work_type%5B0%5D/SOU/work_t" \
              u"ype_name%5B0%5D/音声/per_page/30"

if mode == 0:
    urlNAME = u'''https://www.dlsite.com/maniax/fsr/=/keyword_creater/"{0}"'''.format(name)
elif mode == 2:
    urlNAME = u"https://www.dlsite.com/maniax/fsr/=/language/jp/sex_category%5B0%5D/male/keyword/" + name

partList = [0,2]


# pageNAME = requests.post(urlNAME, proxies=proxies, headers=headers)
while True:
    try:
        pageNAME = requests.post(urlNAME, headers=headers,timeout=5)
        break
    except Exception as e:
        print(e)
        continue
soupNAME = BeautifulSoup(pageNAME.text, features="lxml")

# idRex = re.compile("^https://www.dlsite.com/(maniax|pro)/work/=/product_id.*")
dtRex = re.compile("^_link_.*")
idRex = re.compile("^https://www.dlsite.com/.*/work/=/product_id.*")
typeRex = re.compile("^https://.*_type.*")
allNumberList = soupNAME.find_all(name='div', class_="page_total")
dtList = soupNAME.find_all(name='dt', id=dtRex, class_=True)
otherPageList = soupNAME.find_all(name='td', class_="page_no")
otherPageList = otherPageList[0].find_all(name='a')
if otherPageList:
    otherPageLink = otherPageList[0]["href"]

allNumber = int(allNumberList[0].strong.string)

if mode in partList:
    allCode = {}
elif mode ==1:
    allCode = []

def addCode(allCode,dtList):
    if mode in partList:
        for dtLable in dtList:
            linkLableList = dtLable.find_all(name='a', href=idRex)
            code = linkLableList[0]["href"][-13:-5]
            typeLableList = dtLable.find_all(name='a', href=typeRex)
            workType = typeLableList[0].string.replace("/","／")
            if not workType in allCode:
                allCode[workType]=[]
            allCode[workType].append(code)
    elif mode == 1:
        for dtLable in dtList:
            linkLableList = dtLable.find_all(name='a', href=idRex)
            allCode.append(linkLableList[0]["href"][-13:-5])

print(urlNAME)
print(len(dtList))
addCode(allCode,dtList)

def analysLink(url):
    print(url)
    #page = requests.post(lotPageURL, proxies=proxies, headers=headers)
    while True:
        try:
            page = requests.post(url, headers=headers,timeout=5)
            break
        except Exception as e:
            print(e)
            continue
    soup = BeautifulSoup(page.text, features="lxml")
    dtList = soup.find_all(name='dt', id=dtRex, class_=True)
    print(len(dtList))
    return dtList

def OtherP(otherPageLink):
    if allNumber % 30 == 0:
        end = allNumber // 30
    else:
        end = allNumber // 30 + 1
    for j in range(2, end + 1):
        otherPageURL = otherPageLink[:-1] + str(j)
        otherPageDtList = analysLink(otherPageURL)
        addCode(allCode,otherPageDtList)

if allNumber > 30:
    OtherP(otherPageLink)

def write(allCode):
    if mode in partList:
        for t in allCode:
            with open(name + u"_" + t + u".txt", "w") as f:
                for i in sorted(allCode[t]):
                    f.write(i + "\n")
    elif mode == 1:
        with open(filename + u"_Code.txt", "w") as f:
            for i in allCode:
                f.write(i + "\n")


write(allCode)


print("all=" + str(allNumber))
getNum = 0
if mode in partList:
    for t in allCode:
        getNum += len(allCode[t])
elif mode == 1:
    getNum = len(allCode)
print("get=" + str(getNum))