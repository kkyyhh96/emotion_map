# coding:utf-8
# version:python3.5.1
# author:kyh

import psycopg2
import requests
import httplib, urllib, base64
import json


class emotion_face():
    def __init__(self, id, site, anger, contempt, disgust, fear, happiness, neutral, sadness, surprise):
        self.id = id
        self.site = site
        self.anger = anger
        self.contempt = contempt
        self.disgust = disgust
        self.fear = fear
        self.happiness = happiness
        self.neutral = neutral
        self.sadness = sadness
        self.surprise = surprise

    def input_emotion(self, connection, cursor):
        try:
            sql_command_update = ""
            cursor.execute(sql_command_update)
            connection.commit()
            return True
        except Exception as e:
            print(e)
            connection.rollback()
            return False


# 连接数据库
def db_connect():
    try:
        connection = psycopg2.connect(database="EmotionMap", user="postgres",
                                      password="postgres", host="127.0.0.1", port="5432")
        cursor = connection.cursor()
        print("Database Connection has been opened completely!")
        return connection, cursor
    except Exception as e:
        print(e)


# 查询存在人脸的照片
def query_photo(connection, cursor):
    sql_command_select = "SELECT * FROM photo WHERE f_hasface='TRUE' LIMIT 1"
    cursor.execute(sql_command_select)
    photo = cursor.fetchone()
    # 如果存在这样的照片,记录url
    if photo is not None:
        photo_id = photo[0]
        photo_url = photo[1]
        photo_site = photo[3]
        sql_command_update = "UPDATE photo SET start_recog='TRUE' WHERE id={0}".format(photo_id)
        cursor.execute(sql_command_update)
        connection.commit()
        return id, photo_url, photo_site
    # 不存在这样的地点,说明已经全部识别完毕
    else:
        return None


# 情绪识别
def emotion_recognition(url):
    # Image to analyse (body of the request)
    body = '{\'URL\': \'' + url + '\'}'
    # API request for Emotion Detection
    headers = {'Content-type': 'application/json', }
    params = urllib.urlencode({'subscription-key': 'ad946a803d384c379690cb42eff4e0ed', })  # Enter EMOTION API key
    try:
        # Send httpquest
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
        response = conn.getresponse()
        emotion_info = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return emotion_info


def emotion_input(emotion_info, id, site, connection, cursor):
    emotions = json.loads(emotion_info)
    for emotion in emotions:
        anger = emotion['scores']['anger']
        contempt = emotion['scores']['contempt']
        disgust = emotion['scores']['disgust']
        fear = emotion['scores']['fear']
        happiness = emotion['scores']['happiness']
        neutral = emotion['scores']['neutral']
        sadness = emotion['scores']['sadness']
        surprise = emotion['scores']['surprise']
        face = emotion_face(id, site, anger, contempt, disgust, fear, happiness, neutral, sadness, surprise)
        return face.input_emotion(connection, cursor)


def __main__():
    connection, cursor = db_connect()
    id, url, site = query_photo(connection, cursor)
    emotion_info = emotion_recognition(url)
    emotion_input(emotion_info, id, site, connection, cursor)


__main__()
