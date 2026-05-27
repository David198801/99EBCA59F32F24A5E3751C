import os

year = "2017"
trans = [113,209]

def checkDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

correctList = ["2000","2003","2007"]
if year == "2000":
    # correctDays = [112,113,114,120,121,122,128,129,130]
    correctDays = [114,122,130]
elif year == "2003":
    correctDays = [114,122,130]
elif year == "2007":
    correctDays = [112,113,114,121,128,129,130]