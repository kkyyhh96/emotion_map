import httplib, urllib, base64
import json

def getJson(url):
   # Image to analyse (body of the request)
   body = '{\'URL\': \''+url+'\'}'
   # API request for Emotion Detection
   headers = {'Content-type': 'application/json',}
   params = urllib.urlencode({ 'subscription-key': 'ad946a803d384c379690cb42eff4e0ed',})  # Enter EMOTION API key
   try:
       #Send httpquest
      conn = httplib.HTTPSConnection('api.projectoxford.ai')
      conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
      response = conn.getresponse()
      data = response.read()
      print(data)
      conn.close()
   except Exception as e:
      print("[Errno {0}] {1}".format(e.errno, e.strerror))
   return data

#Input file name
location="6GrandCentralTerminal"
readPath="//home//version2//flickr//2//"
savePath="//home//version2//face++//2//"
file = open(readPath+location + r'Face.txt', 'r')
lines=file.readlines()
file.close()
for line in lines:
    url=line.split(',')[0]
    date=line.split(',')[1].split('\n')[0]
    try:
        data=getJson(url)
        dataJsonList=json.loads(data)
        for dataJson in dataJsonList:
            anger=dataJson['scores']['anger']
            contempt=dataJson['scores']['contempt']
            disgust=dataJson['scores']['disgust']
            fear=dataJson['scores']['fear']
            happiness=dataJson['scores']['happiness']
            neutral=dataJson['scores']['neutral']
            sadness=dataJson['scores']['sadness']
            surprise=dataJson['scores']['surprise']

            file = open(str(savePath) +location+ r'Emotion.txt', 'a')
            file.write(str(url)+","+str(date)+","+str(anger)+","+str(contempt)+","+str(disgust)+","+str(fear)+
                       ","+str(happiness)+","+str(neutral)+","+str(sadness)+","+str(surprise)+"\n")
            file.close()
    except Exception as e:
        print(str(e))
	file = open(str(savePath) + location + r'Error.txt', 'a')
        file.write(line)
        file.close()

file = open(savePath+location + r'Error.txt', 'r')
lines=file.readlines()
file.close()
file = open(savePath+location + r'Error.txt', 'w')
file.write('')
file.close()
for line in lines:
    url=line.split(',')[0]
    date=line.split(',')[1].split('\n')[0]
    try:
        data=getJson(url)
        dataJsonList=json.loads(data)
        for dataJson in dataJsonList:
            anger=dataJson['scores']['anger']
            contempt=dataJson['scores']['contempt']
            disgust=dataJson['scores']['disgust']
            fear=dataJson['scores']['fear']
            happiness=dataJson['scores']['happiness']
            neutral=dataJson['scores']['neutral']
            sadness=dataJson['scores']['sadness']
            surprise=dataJson['scores']['surprise']

            file = open(str(savePath) +location+ r'Emotion.txt', 'a')
            file.write(str(url)+","+str(date)+","+str(anger)+","+str(contempt)+","+str(disgust)+","+str(fear)+
                       ","+str(happiness)+","+str(neutral)+","+str(sadness)+","+str(surprise)+"\n")
            file.close()
    except Exception as e:
        print(str(e))
	file = open(str(savePath) + location + r'Error.txt', 'a')
        file.write(line)
        file.close()

file = open(savePath+location + r'Error.txt', 'r')
lines=file.readlines()
file.close()
file = open(savePath+location + r'Error.txt', 'w')
file.write('')
file.close()
for line in lines:
    url=line.split(',')[0]
    date=line.split(',')[1].split('\n')[0]
    try:
        data=getJson(url)
        dataJsonList=json.loads(data)
        for dataJson in dataJsonList:
            anger=dataJson['scores']['anger']
            contempt=dataJson['scores']['contempt']
            disgust=dataJson['scores']['disgust']
            fear=dataJson['scores']['fear']
            happiness=dataJson['scores']['happiness']
            neutral=dataJson['scores']['neutral']
            sadness=dataJson['scores']['sadness']
            surprise=dataJson['scores']['surprise']

            file = open(str(savePath) +location+ r'Emotion.txt', 'a')
            file.write(str(url)+","+str(date)+","+str(anger)+","+str(contempt)+","+str(disgust)+","+str(fear)+
                       ","+str(happiness)+","+str(neutral)+","+str(sadness)+","+str(surprise)+"\n")
            file.close()
    except Exception as e:
        print(str(e))
	file = open(str(savePath) + location + r'Error.txt', 'a')
        file.write(line)
        file.close()

file = open(str(savePath) + location + r'Finish.txt', 'a')
file.close()
