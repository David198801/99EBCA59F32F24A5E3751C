import re
pattern=re.compile(r'^(?!if.*)$')
pattern2=re.compile(r'^(?!.*helloworld).*$')
print pattern.match('aaif')
print pattern.match('xxxxxhellorld')
print pattern.match('hellorldxxxxxx')