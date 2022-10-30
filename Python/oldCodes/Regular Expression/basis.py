import re
pattern = re.compile(r'he')
match = pattern.match('helloworld!')
if match:
    print match.group()
else:
    print match