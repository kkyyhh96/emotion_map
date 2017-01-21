# coding:utf-8
# version:python3.5.1
# author:kyh

import psycopg2
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json


class emotion_face():
    def __init__(self, id, site, anger, contempt, disgust, fear, happiness, neutral, sadness, surprise):
        self.photo_id = id
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
        sql_command_query = "SELECT COUNT(id) FROM ms_emotion"
        cursor.execute(sql_command_query)
        face_count = cursor.fetchone()[0]
        try:
            sql_command_update = "INSERT INTO ms_emotion VALUES({0},{1},'{2}',{3},{4},{5},{6},{7},{8},{9},{10})".format(
                face_count+1, self.photo_id, self.site, self.anger, self.contempt, self.disgust, self.fear,
                self.happiness, self.neutral, self.sadness, self.surprise)
            cursor.execute(sql_command_update)
            connection.commit()
            print("Insert Success!")
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
    sql_command_select = "SELECT id,url,site FROM photo WHERE f_hasface='TRUE' LIMIT 1"
    cursor.execute(sql_command_select)
    photo = cursor.fetchone()
    # 如果存在这样的照片,记录url
    if photo is not None:
        photo_id = photo[0]
        photo_url = photo[1]
        photo_site = photo[2]
        sql_command_update = "UPDATE photo SET start_recog='TRUE' WHERE id={0}".format(photo_id)
        cursor.execute(sql_command_update)
        connection.commit()
        return photo_id, photo_url, photo_site
    # 不存在这样的地点,说明已经全部识别完毕
    else:
        return None, None, None


# 情绪识别
def emotion_recognition(url):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        # 'Ocp-Apim-Subscription-Key': '32523fc34d5f44769b0f37309bd9ba7c',
        'Ocp-Apim-Subscription-Key': '7cefe0616f6d4354a0660b12b83811d8',
    }
    body = '{\'URL\':\'' + url + '\'}'
    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        #conn = http.client.HTTPSConnection('api.cognitive.azure.cn')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data.decode()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def emotion_input(emotion_info, id, site, connection, cursor):
    try:
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
    except Exception as e:
        print(e)


# 关闭数据库
def close_connection(connection):
    try:
        connection.close()
        print("Database Connection has been closed completely!")
        return True
    except Exception as e:
        print(e)


def __main__():
    connection, cursor = db_connect()
    id, url, site = query_photo(connection, cursor)
    while id is not None:
        emotion_info = emotion_recognition(url)
        emotion_input(emotion_info, id, site, connection, cursor)
        id, url, site = query_photo(connection, cursor)
    close_connection(connection, cursor)


__main__()
