#coding:utf-8
#python2.7
from facepp import API
import json

api_key='14d6d4c65fe5d7739db529369110b5ca'
api_secret='s5u3SLNzD5lCMyHioXKFOvsYx-jCl4Wl'
api=API(api_key,api_secret)

locationName='49PalaceOfVersailles'
path="//home//version2//flickr//10//"
dataPath=path+locationName+'.txt'
facePath=path+locationName+'Face.txt'
errorPath=path+locationName+'Error.txt'
finishPath=path+locationName+'Finish.txt'

def faceDetect(lines):
    count=0
    for line in lines:
        try:
            count+=1
            urlPic=line.split(',')[0]
            date=line.split(',')[1]
            print str(count)+"."+line.split('\n')[0]
            face=api.detection.detect(url=urlPic)
            length=len(face['face'])
            if length>0:
                faceFile=open(facePath,'a')
				faceFile.write(line)
				faceFile.close()
                print("Write Success!")
            else:
                print("Detect Success!While no face!")
        except Exception as e:
            print(str(e))
            print("Write Failed!Something may be error!")
            errorFile=open(errorPath,'a')
            errorFile.write(line)
            errorFile.close()

File=open(dataPath,'r')
lines1=File.readlines()
File.close()
faceDetect(lines1)

File=open(errorPath,'r')
lines2=File.readlines()
File.close()
File=open(errorPath,'w')
File.write('')
File.close()
faceDetect(lines2)

File=open(errorPath,'r')
lines3=File.readlines()
File.close()
File=open(errorPath,'w')
File.write('')
File.close()
faceDetect(lines3)

File=open(finishPath,'w')
File.close()
print("All Success!")

