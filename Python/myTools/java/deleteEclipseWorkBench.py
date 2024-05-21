#coding:utf-8
import os
import shutil

path="X:\\"

for i in os.listdir(path):
    deletePath = os.path.join(path,i)
    if os.path.isdir(deletePath) and i.startswith("workspace"):
        deletePath = os.path.join(deletePath,".metadata")
        deletePath = os.path.join(deletePath,".plugins")
        deletePath = os.path.join(deletePath,"org.eclipse.ui.workbench")
        if os.path.exists(deletePath):
            shutil.rmtree(deletePath)
        print(deletePath)