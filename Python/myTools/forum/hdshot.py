import requests
import time

url = r"https://www.hdshot.net/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1"

headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
"Content-Length":"56",
"Content-Type":"application/x-www-form-urlencoded",
"Cookie":"LNI3_2132_saltkey=DNyQ8Bzn; LNI3_2132_lastvisit=1599469607; LNI3_2132_study_nge_extstyle=1; LNI3_2132_study_nge_extstyle_default=1; LNI3_2132_nofavfid=1; LNI3_2132_smile=1D1; LNI3_2132_forum_lastvisit=D_43_1599619807D_50_1599635699D_38_1599650074; LNI3_2132_visitedfid=43D38D46D80D37D108D36D50; LNI3_2132_sid=ig63M3; LNI3_2132_viewid=tid_6768; LNI3_2132_sendmail=1; LNI3_2132_seccode=104.4de8301a79db55cc7d; LNI3_2132_ulastactivity=e5140ZBsZVGoEQ7iZhM9tMHppCA0opnCj2AaBWRQ8LnuINJJhscV; LNI3_2132_auth=5d77JqpF3c2%2FVHPIpEgqzvv9oJLiggHuFPdQdBzYr8W3BbXMac%2BlkSRO61IB135ducIIYKjqZs5zIZi5mWsp6Ntk; LNI3_2132_lastcheckfeed=4504%7C1599714943; LNI3_2132_checkfollow=1; LNI3_2132_st_p=4504%7C1599714945%7Ce2a7645e7a4bc27b673d5ad7395109ce; LNI3_2132_checkpm=1; LNI3_2132_lastact=1599714946%09plugin.php%09",
"Host":"www.hdshot.net",
"Origin":"https//www.hdshot.net",
"Referer":"https//www.hdshot.net/thread-6768-1-1.html",
"Sec-Fetch-Mode":"nested-navigate",
"Sec-Fetch-Site":"same-origin",
"Sec-Fetch-User":"?1",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}


def main()
    r = requests.post(url,headers = headers)