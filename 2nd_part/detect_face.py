# coding:utf-8
# version:python3.5.1
# author:kyh

import psycopg2
import requests
import json

# face++的人脸
class facepp_face():
    def __init__(self, photo_id, site, gender, age, smile, glass):
        self.photo_id = photo_id
        self.site = site
        self.gender = gender
        self.age = age
        self.smile = smile
        self.glass = glass

    def input_face(self):
        print("hello")


# 连接数据库
def db_connect():
    connection = psycopg2.connect(database="EmotionMap", user="postgres",
                                  password="postgres", host="127.0.0.1", port="5432")
    cursor = connection.cursor()
    return connection, cursor


# face++API
def faceppAPI(url):
    facepp_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    api_key = 'iExD00qRzPaOm9lSFKhLMuKq-fVrs9pW'
    api_secret = 'B6_36b807WxgYLOTgjP94sc_QanKp-9T'
    try:
        params = dict(api_key=api_key, api_secret=api_secret, image_url=url,return_landmark=1,return_attributes="gender,age,smiling,glass,headpose,facequality,blur")
        result = requests.post(url=facepp_url, params=params,timeout=15)
        return result.text
    except Exception as e:
        print(e)
        return None


# 查询没被检测过人脸的照片
def photo_detect(db_connection, db_cursor):
    sql_command_select = "SELECT id,url FROM photo WHERE start_detect=FALSE LIMIT 1"
    db_cursor.execute(sql_command_select)
    photo = db_cursor.fetchone()
    if photo is not None:
        photo_id = photo[0]
        photo_url = photo[1]
        try:
            sql_command_update = "UPDATE photo SET start_detect='TRUE' WHERE id={0}".format(photo_id)
            db_cursor.execute(sql_command_update)
            db_connection.commit()
            return photo_id, photo_url
        except Exception as e:
            print(e)
            db_connection.rollback()
            return None, None
    else:
        return None, None


# 探测人脸
def face_detect(id,photo_url):
    result = faceppAPI(photo_url)
    if result is not None:
        faces=json.loads(result)["faces"]
        for each_face in faces:
            face=facepp_face(id,)

def __main__():
    connection, cursor = db_connect()
    id, url = photo_detect(connection, cursor)
    #face_detect(id,url)
    face_detect(id,"http://bj-mc-prod-asset.oss-cn-beijing.aliyuncs.com/mc-official/images/face/demo-pic6.jpg")


__main__()
