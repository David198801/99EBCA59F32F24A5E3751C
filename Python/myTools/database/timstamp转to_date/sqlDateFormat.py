import win32clipboard
import win32con
import re

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

pattern = re.compile(r"TIMESTAMP '(.{19})\..{6}'")

def repl(matched):
    if matched:
        d = matched.group(1)
        return "TO_DATE('"+d+"','YYYY-MM-DD HH24:mi:ss')"

while True:
    text = get_text()
    newText = re.subn(pattern,repl,text)
    print(newText)
    set_text(newText[0])
    input("替换成功")
