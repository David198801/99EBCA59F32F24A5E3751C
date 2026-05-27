import win32clipboard
import win32con
import re
from datetime import datetime

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

pattern = r"^\d{4}-\d{2}-\d{2}$"
def fill_date(date_str,sql):
    if re.match(pattern, date_str):
        sql = sql.replace('?', "date\'"+date_str+"\'", 1)
        return sql
        
    try:
        # 解析日期字符串，格式为 "Tue May 20 00:00:00 CST 2025"
        date_obj = datetime.strptime(date_str, "%a %b %d %H:%M:%S CST %Y")
        # 转换为 "YYYY-MM-DD" 格式
        date_format = date_obj.strftime("%Y-%m-%d")
        sql = sql.replace('?', "date\'"+date_format+"\'", 1)
        return sql
    except ValueError:
        # 如果字符串不符合预期格式，则返回错误信息
        return None

while True:
    input("请复制SQL参数并按回车：")
    params = get_text()
    input("请复制SQL并按回车：")
    sql = get_text()
    
    params = params.strip()[1:-1].split(",")
    for param in params:
        param = param.strip()
        
        temp = fill_date(param,sql)
        if temp:
            sql = temp
            continue
            
        sql = sql.replace('?', "\'"+param+"\'", 1)
        
        set_text(sql)
        print("替换结果：" + sql)
        print("")
            
            
            