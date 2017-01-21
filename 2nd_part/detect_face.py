# coding:utf-8
# version:python3.5.1
# author:kyh

import psycopg2
import requests
import json


# face++的人脸
class facepp_face():
    def __init__(self, photo_id, site, gender, age, smile, smile_threshold, glass):
        self.photo_id = photo_id
        self.site = site
        if gender == "Male":
            self.gender = 0
        else:
            self.gender = 1
        self.age = age
        self.smile = smile
        self.smile_threshold = smile_threshold
        self.glass = glass

    def input_face(self, db_connection, db_cursor):
        try:
            sql_command_query = "SELECT COUNT(id) FROM facepp"
            db_cursor.execute(sql_command_query)
            face_count = db_cursor.fetchone()[0]
            sql_command_insert = "INSERT INTO facepp VALUES({0},{1},'{2}',{3},{4},{5},{6},'{7}')".format(face_count + 1,
                                                                                                         self.photo_id,
                                                                                                         self.site,
                                                                                                         self.gender,
                                                                                                         self.age,
                                                                                                         self.smile,
                                                                                                         self.smile_threshold,
                                                                                                         self.glass)
            db_cursor.execute(sql_command_insert)
            sql_command_modify = "UPDATE photo SET f_hasface=TRUE WHERE id={0}".format(self.photo_id)
            db_cursor.execute(sql_command_modify)
            db_connection.commit()
            print("Success insert face!")
        except Exception as e:
            print(e)
            db_connection.rollback()
            return False


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
        params = dict(api_key=api_key, api_secret=api_secret, image_url=url, return_landmark=1,
                      return_attributes="gender,age,smiling,glass")
        result = requests.post(url=facepp_url, params=params, timeout=15)
        return result.text
    except Exception as e:
        print(e)
        return None


# 查询没被检测过人脸的照片
def photo_detect(db_connection, db_cursor):
    sql_command_select = "SELECT id,url,site FROM photo WHERE start_detect=FALSE LIMIT 1"
    db_cursor.execute(sql_command_select)
    photo = db_cursor.fetchone()
    if photo is not None:
        photo_id = photo[0]
        photo_url = photo[1]
        photo_site = photo[2]
        try:
            sql_command_update = "UPDATE photo SET start_detect='TRUE' WHERE id={0}".format(photo_id)
            db_cursor.execute(sql_command_update)
            db_connection.commit()
            return photo_id, photo_url, photo_site
        except Exception as e:
            print(e)
            db_connection.rollback()
            return None, None, None
    else:
        return None, None


# 探测人脸
def face_detect(db_connection, db_cursor, id, photo_url, photo_site):
    result = faceppAPI(photo_url)
    try:
        if result is not None:
            faces = json.loads(result)["faces"]
            for face_info in faces:
                each_face = face_info["attributes"]
                face_gender = each_face["gender"]["value"]
                face_age = each_face["age"]["value"]
                face_smile = each_face["smile"]["value"]
                face_smile_threshold = each_face["smile"]["threshold"]
                face_glass = each_face["glass"]["value"]
                face = facepp_face(id, photo_site, face_gender, face_age, face_smile, face_smile_threshold, face_glass)
                return face.input_face(db_connection, db_cursor)
    except Exception as e:
        print(e)
        return None


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
    id, url, site = photo_detect(connection, cursor)
    while id is not None:
        face_detect(connection, cursor, id, url, site)
        id, url, site = photo_detect(connection, cursor)
    # face_detect(connection, cursor, id,
    #            "http://bj-mc-prod-asset.oss-cn-beijing.aliyuncs.com/mc-official/images/face/demo-pic6.jpg", "a")
    close_connection(connection)
    print("All faces has been detected!")


__main__()
