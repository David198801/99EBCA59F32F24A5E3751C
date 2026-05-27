#coding:UTF-8
import jsbeautifier

path='A.JS'

encoding='UTF-8'

beautified_code=''
with open(path, 'r',encoding=encoding) as file:
    data = file.read()
    beautified_code = jsbeautifier.beautify(data)
with open(path, 'w',encoding=encoding) as file:
    file.write(beautified_code)

