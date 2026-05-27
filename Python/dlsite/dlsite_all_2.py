import requests
from bs4 import BeautifulSoup
import time
import re

base_url = "https://www.dlsite.com/maniax/fsr/=/language/jp/sex_category%5B0%5D/male/ana_flg/off/order%5B0%5D/trend/work_type%5B0%5D/SOU/work_type_name%5B0%5D/%E9%9F%B3%E5%A3%B0%E3%83%BBASMR/genre_and_or/or/options_and_or/or/per_page/100/show_type/1/page/{0}"
all_page_num = 196
all_page_num_str = str(all_page_num)
rj_set = set()


headers = {"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"accept-encoding":"gzip, deflate, br",
"accept-language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5",
"cache-control":"max-age=0",
#"cookie":"dlsite_dozen=0; uniqid=3j34j2hkp9; adultchecked=1; _ga=GA1.2.263111392.1575779454; _gaid=263111392.1575779454; _d3date=2019-12-08T043056.843Z; _d3landing=1; adr_id=zCQgeesqV8TaXahgQUawgLnlkiMdn1Ih3iTHiZwyBMFPkhQn; _td=8b749f3f-3101-4041-80ab-445b3d3c5d69; session_state=bd8dfc450b587aece1f77eac41328b01e5407f512116d83a2004ee249b804a58.2emoxea5y328k84cook4k4440; loginchecked=1; DL_STAR_ID=6; utm_c=sns_link; locale=zh-cn; __DLsite_SID=hum7arg8bpbv214jf80qam9asl; DL_SITE_DOMAIN=maniax; DL_PRODUCT_LOG=%2CRJ294105%2CRJ292031%2CRJ291298%2CRJ295582%2CRJ277492.htmlRJ262175%2CRJ194353%2CRJ244855%2CRJ163690%2CRJ175899%2CRJ219051%2CRJ245512%2CRJ247761%2CRJ177905%2CRJ224695%2CRJ227798%2CRJ239939%2CRJ239238%2CRJ233647%2CRJ269164%2CRJ290963%2CRJ083355%2CRJ288853%2CRJ223323%2CRJ185915%2CRJ255109%2CRJ255618%2CRJ269057%2CRJ196062%2CRJ231718%2CRJ220732%2CRJ284644%2CRJ207679%2CRJ282003%2CRJ073920%2CRJ278396%2CRJ147133%2CRJ229226%2CRJ285826%2CVJ007373%2CRJ201848%2CRJ244621%2CRJ226737%2CRJ212704%2CRJ218604%2CRJ149609%2CRJ132683%2CRJ116720%2CRJ262563%2CRJ266712%2CRJ117823",
"sec-fetch-mode":"navigate",
"sec-fetch-site":"same-origin",
"sec-fetch-user":"?1",
"upgrade-insecure-requests":"1",
"user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

rex = re.compile(r'[a-zA-Z]{2}[0-9]{6}')

for page_num in range(1, all_page_num + 1):
    #time.sleep(1)
    page_num_str = str(page_num)
    print('-----------------')
    print('[' + page_num_str + '/' + all_page_num_str + ']')
    print('-----------------')
    url = base_url.format(page_num_str)

    while True:
        try:
            r = requests.get(url, headers=headers,timeout = 10)
            soup = BeautifulSoup(r.text, features="lxml")
            searchDivLableList = soup.find_all(name='div', class_="_search_result_list")
            workALableList = searchDivLableList[0].find_all(name='a')
            break
        except Exception as e:
            print(e)
            continue



    for workALable in workALableList:
        rjCode = workALable["href"].replace(".html","").split("/")[-1]
        if re.match(rex,rjCode):
            #print(rjCode)
            rj_set.add(rjCode)

with open(r"D:\linshi2\dlsite_all111.txt","w") as txt:
    for i in sorted(list(rj_set)):
        txt.write(i+"\n")