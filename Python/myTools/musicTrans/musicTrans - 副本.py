#coding:utf8
import os
import subprocess
import re

musicPath = r"D:\music"
outFormat = "m4a"
setBitrate = '128k'

otherArgsList = []
vbrSwitch = True

if outFormat == "m4a":
    otherArgsList = ['-acodec','libfdk_aac','-profile:a','aac_he_v2']

    
if vbrSwitch:
    vbrArgs = ['-vbr','2']
    otherArgsList += vbrArgs
    setBitrate = 'vbr' + vbrArgs[1]
    
    
flacDirPath = os.path.join(musicPath,"flac")
outDirPath = os.path.join(musicPath,outFormat+setBitrate)

if not os.path.exists(outDirPath):
    os.makedirs(outDirPath)
    


def getFFmpegOut(filePath):
    command = ["ffprobe", "-show_format", "-i", filePath]
    result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = str(result.stdout.read())
    return out
def getBitrate(out):
    rex = re.compile(r".*bitrate: +(\d+) kb.*")
    rm = rex.match(out)
    r =  rm.group(1)
    return int(r)
def getSampleRate(out):
    rex = re.compile(r".+?(\d+) Hz.+")
    rm = rex.match(out)
    r =  rm.group(1)
    return r
def chooseBitrate(n):
    max = int(setBitrate[:-1])
    if n >= max:
        return max
    bitrateList = [64,96,128,192,256,320]
    for i in range(len(bitrateList)):
        if bitrateList[i]>=max:
            bitrateList = bitrateList[:i]
            break
    
    for i in bitrateList:
        if n == i:
            return i
        elif n < i:
            return i
    
for root,dirs,files in os.walk(flacDirPath):
    for f in files:
    
        outBitrate = setBitrate
        flacFilePath = os.path.join(root,f)
        fileExt = f.split(".")[-1]
        
        outFilePath = os.path.join(outDirPath,flacFilePath.replace(flacDirPath,"")[1:])
        outFilePath = outFilePath.replace('.' + fileExt,'.' + outFormat)
        directOutsDirPath = os.path.dirname(outFilePath)
        if not os.path.exists(directOutsDirPath):
            os.makedirs(directOutsDirPath)
            
        if os.path.exists(outFilePath):
            continue
            
        print(outFilePath)
        
        
        
        ffmpegOut = getFFmpegOut(flacFilePath)
        
        sampleRate = getSampleRate(ffmpegOut)
        
        arMark8 = False
        arMark9 = False
        if sampleRate == '88200':
            otherArgsList += ['-ar','44100']
            arMark8 = True
        elif sampleRate == '96000':
            otherArgsList += ['-ar','48000']
            arMark9 = True
            
        if vbrSwitch:
            commandList = ['ffmpeg','-i',flacFilePath] + otherArgsList + [outFilePath]
            print("\n-----------------------------\n")
            print(commandList)
            print("-----------------------------\n")
            subprocess.call(commandList)
            if arMark8:
                otherArgsList.remove('-ar')
                otherArgsList.remove('44100')
            if arMark9:
                otherArgsList.remove('-ar')
                otherArgsList.remove('48000')
            continue
        
        if fileExt == outFormat:
            bitrate = getBitrate(ffmpegOut)
            if bitrate < int(setBitrate[:-1]):
                subprocess.call(['copy',flacFilePath,outFilePath],shell=True)
                continue

        if fileExt != "flac":
            bitrate = getBitrate(ffmpegOut)
            outBitrate = str(chooseBitrate(bitrate)) + 'k'
        commandList = ['ffmpeg','-i',flacFilePath,'-ab',outBitrate]
        if otherArgsList:
            commandList += otherArgsList
        commandList.append(outFilePath)
        print("\n-----------------------------\n")
        print(commandList)
        print("-----------------------------\n")
        subprocess.call(commandList)
        if arMark8:
            otherArgsList.remove('-ar')
            otherArgsList.remove('44100')
        if arMark9:
            otherArgsList.remove('-ar')
            otherArgsList.remove('48000')

            
        
        
        
