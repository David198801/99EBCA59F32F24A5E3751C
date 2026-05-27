from bs4 import BeautifulSoup
import re

rex = re.compile(r"^https://v.youku.com/v_show/id_.+")

h = r"C:\Users\Administrator\Desktop\a.html"
htmlfile = open(h, 'r', encoding='utf-8')
b  = BeautifulSoup(htmlfile.read(), features="lxml")
link = b.find_all(name="a",href=rex)
for i in link:
    print(i["href"])
