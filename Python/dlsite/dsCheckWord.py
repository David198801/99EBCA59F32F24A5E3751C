import requests
import os

path = r"E:\音声\御崎ひより"
word = r"めぐり逢音"
l = os.listdir(path)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

for i in l:
    if i[:2].upper()=="RJ":
        rjCode = i[:8]
        url = r"https://www.dlsite.com/maniax/work/=/product_id/" + rjCode
        while True:
            try:
                r = requests.post(url,headers=headers, timeout=5)
                break
            except Exception as e:
                print(e)
                continue
        if word in r.text:
            print(rjCode)