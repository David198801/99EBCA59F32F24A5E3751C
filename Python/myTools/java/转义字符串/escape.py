import win32clipboard
import win32con

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

def escape(s):
    return s.replace('"',r'\"').replace('\r\n',r'\n')

set_text(escape(get_text()))

