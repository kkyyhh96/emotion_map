# coding:utf-8
# version:python3.5.1
# author:kyh

import http.client
import json
import urllib.error
import urllib.parse
import urllib.request

import psycopg2


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
            sql_command_insert = "INSERT INTO ms_emotion(photo_id,site,anger,contempt,disgust," \
                                 "fear,happiness,neutral,sadness,surprise) " \
                                 "VALUES ({0},'{1}',{2},{3},{4},{5}," \
                                 "{6},{7},{8},{9});".format(
                self.id, self.site, self.anger, self.contempt, self.disgust, self.fear, self.happiness,
                self.neutral, self.sadness, self.surprise
            )
            cursor.execute(sql_command_insert)
            connection.commit()
            print("Success!")
            return True
        except Exception as e:
            print(e)
            connection.rollback()
            return False


# 连接数据库
def db_connect():
    try:
        connection = psycopg2.connect(database="StockMap", user="postgres",
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
        return photo_id, photo_url, photo_site
    # 不存在这样的地点,说明已经全部识别完毕
    else:
        return None, None, None


# 情绪识别
def emotion_recognition(url):
    body = '{\'URL\': \'' + str(url) + '\'}'
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '7cefe0616f6d4354a0660b12b83811d8',
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        # 返回情绪值
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        # 发生错误，返回None
        return None


# 提取情绪值
def emotion_input(emotion_info, id, site, connection, cursor):
    emotion_info = emotion_info.decode()
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
        #如果id不为空,则探测人脸情绪
        emotion_info = emotion_recognition(url)
        count = 0
        #如果情绪出错,则重复3次探测
        while emotion_info is None and count <= 3:
            emotion_info = emotion_recognition(url)
            count += 1
        #如果情绪不出错,则输入数据库中
        if emotion_info is not None:
            if emotion_input(emotion_info, id, site, connection, cursor) is False:
                emotion_info(emotion_info, id, site, connection, cursor)
    close_connection(connection)


__main__()
