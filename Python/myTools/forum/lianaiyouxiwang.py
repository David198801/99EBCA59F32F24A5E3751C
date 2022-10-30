import requests

url = r"https://www.lianaiyx.com/e/member/sign/?doajax=1&ajaxarea=sign"

headers = {"Accept":"*/*",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5",
"Connection":"keep-alive",
"Content-Type":"application/x-www-form-urlencoded",
"Cookie":"zabvsecookieclassrecord=%2C1%2C; zabvsmlusername=admin; zabvsmluserid=1060595; zabvsmlgroupid=1; zabvsmlrnd=iQHdEaKfWGTjHYewqyxD; zabvsmlauth=d0dd8ee0583c5b5c760c5193dcd9a7ff; zabvsm_useronline=1",
"Host":"www.lianaiyx.com",
"Referer":"https//www.lianaiyx.com/e/member/cp/",
"Sec-Fetch-Mode":"cors",
"Sec-Fetch-Site":"same-origin",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}



requests.get(url,headers = headers)