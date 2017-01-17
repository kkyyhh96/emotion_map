# coding:utf-8
# version:python3.5.1
# author:kyh

import psycopg2
import requests


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
    sql_command_select = "SELECT * " \
                         "FROM photo " \
                         "WHERE f_hasface=='TRUE'"

    cursor.execute(sql_command_select)
    photo = cursor.fetchone()
    # 如果存在这样的照片,记录url
    if photo is not None:
        photo_id = photo[0]
        photo_url = photo[1]
        sql_command_update = "UPDATE photo " \
                             "SET start_recog='TRUE' " \
                             "WHERE id=='" + str(photo_id) + "'"
        cursor.execute(sql_command_update)
        connection.commit()
        return photo_url
    # 不存在这样的地点,说明已经全部识别完毕
    else:
        return None


# 情绪识别
def emotion_recognition(url):
    request = requests.post(url=url, params)
