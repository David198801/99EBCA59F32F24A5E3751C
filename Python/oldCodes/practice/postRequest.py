import requests
import os

mid="381828390"

url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid={0}&page=1&pagesize=25".format(mid)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

page = requests.get(url, headers=headers)

def printAV(js):
    jo = js
    l = jo["data"]['vlist']
    for i in l:
        print("av" + str(i['aid']))
    return jo["data"]['count']

n = printAV(page.json())

if n > 25:
    for i in range(2,n/25+2):
        url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid={0}&page={1}&pagesize=25".format(mid,i)
        page = requests.get(url, headers=headers)
        printAV(page.json())