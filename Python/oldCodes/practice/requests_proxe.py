import requests
import re
from bs4 import BeautifulSoup

proxies = {
  "http": "http://127.0.0.1:1088",
  "https": "http://127.0.0.1:1088",
}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

url = "https://www.dlsite.com/maniax/work/=/product_id/RJ206013"


for i in folderLableList:
  print i.string

