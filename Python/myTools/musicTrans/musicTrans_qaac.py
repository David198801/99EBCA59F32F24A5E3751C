#coding:utf8
import os
import subprocess
import re

musicPath = r"D:\music"
qaacPath = r"D:\P\qaac2.71\qaac64\qaac64.exe"
outFormat = "m4a"
setBitrate = '256k'


otherArgsList = []

    
    
flacDirPath = os.path.join(musicPath,"flac")
outDirPath = os.path.join(musicPath,'qaac'+setBitrate)

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
        
        if fileExt == outFormat:
            bitrate = getBitrate(ffmpegOut)
            if bitrate < int(setBitrate[:-1]):
                subprocess.call(['copy',flacFilePath,outFilePath],shell=True)
                continue

        if fileExt != "flac":
            bitrate = getBitrate(ffmpegOut)
            outBitrate = str(chooseBitrate(bitrate)) + 'k'
            
        metaFilePath = os.path.join(outDirPath,'FFMETADATAFILE.meta')
        metaCmdList = ['ffmpeg','-i',flacFilePath,'-f','ffmetadata',metaFilePath]
        subprocess.call(metaCmdList)

        commandList = ['ffmpeg','-i',flacFilePath,'-ab',outBitrate]
        if otherArgsList:
            commandList += otherArgsList
        wavPath = os.path.join(outDirPath,"wavtemp.wav")
        commandList.append(wavPath)
        print("\n-----------------------------\n")
        print(commandList)
        print("-----------------------------\n")
        subprocess.call(commandList)
        
        
        m4aTempPath = os.path.join(outDirPath,"m4atemp.m4a")
        qaacCmdList = [qaacPath,
                        wavPath,'--ignorelength','--threading','-c',outBitrate[:-1],'-o',m4aTempPath]
        subprocess.call(qaacCmdList)
                        
        
        metaCmdList = ['ffmpeg','-i',m4aTempPath,"-i",metaFilePath,"-map_metadata","1",
                        "-codec","copy",outFilePath]
        subprocess.call(metaCmdList)
        
        os.remove(m4aTempPath)
        os.remove(wavPath)
        os.remove(metaFilePath)
        
        
        if arMark8:
            otherArgsList.remove('-ar')
            otherArgsList.remove('44100')
        if arMark9:
            otherArgsList.remove('-ar')
            otherArgsList.remove('48000')
        

            
        
        
        
