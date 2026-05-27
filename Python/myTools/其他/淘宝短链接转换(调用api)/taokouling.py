#coding:utf8
import win32clipboard
import win32con
import re
import requests
import webbrowser
import json

def get_text():
    win32clipboard.OpenClipboard()
    text = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    return text
def set_text(string):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, string)
    win32clipboard.CloseClipboard()


text = get_text()
taokouling = re.search(r'[A-Za-z0-9]{11}',text ).group()


url = r"https://api.taokouling.com/tkl/tkljm?apikey=PhAmVOdDre&tkl=" + taokouling
r = requests.get(url)
d = json.loads(r.text)

webbrowser.open(d["url"])

