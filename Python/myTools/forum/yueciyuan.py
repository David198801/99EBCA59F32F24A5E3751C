import requests

url = r"https://www.abooky.com/plugin.php?id=k_misign:sign&operation=qiandao&formhash=b12153d1&format=empty&inajax=1&ajaxtarget=JD_sign"

headers = {'accept':'*/*',
"accept-encoding":"gzip, deflate, br",
"accept-language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5",
"cookie":"GEj6_2132_connect_is_bind=0; GEj6_2132_nofavfid=1; GEj6_2132_smile=1D1; GEj6_2132_saltkey=m6xfGx8Q; GEj6_2132_lastvisit=1593668154; GEj6_2132_auth=92c38yo6GigCmhdbfZh9XOfKfnOKntQmc%2FooWuInlfwpUZ1DII6FVoJc8As; GEj6_2132_lastcheckfeed=393011%7C1593671784; popnotice=s1040; __cfduid=d55c276ce99708d57d53c97ba9be105671593672281; GEj6_2132_visitedfid=37D38D50D40D43D2D39; GEj6_2132_sid=g28QJZ; GEj6_2132_lip=140.240.28.1%2C1594819546; PHPSESSID=0ta1u80trpf2hunj6vqhgevsv2; GEj6_2132_popadv=a%3A0%3A%7B%7D; GEj6_2132_ulastactivity=bfdfpyuVMnFaydiseYQAJGvodEF1Ozyim09iOk7aoRqHbrEDiIlj; GEj6_2132_sendmail=1; GEj6_2132_lastact=1594873661%09home.php%09spacecp; GEj6_2132_checkpm=1",
"referer":"https//www.abooky.com/plugin.php?id=k_misignsign",
"sec-fetch-mode":"cors",
"sec-fetch-site":"same-origin",
"user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
"x-requested-with":"XMLHttpRequest"}

def yueciyuan():
    r = requests.get(url,headers = headers)
    
yueciyuan()