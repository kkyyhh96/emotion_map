# coding:utf-8
# version:python3.5.1
# author:kyh

import json

import psycopg2
import requests


# 连接数据库
def db_connect():
    connection = psycopg2.connect(database="EmotionMap", user="postgres",
                                  password="postgres", host="127.0.0.1", port="5432")
    cursor = connection.cursor()
    return connection, cursor


# face++API,如果存在人脸,返回True,否则返回False
def faceppAPI(url):
    facepp_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    try:
        params = {
            "api_key": "ca21aa8b4624eb745d683da3e09e0b0c",
            "api_secret": "jwkFQK9hMkVqI1TliYDLKxZBzSkVFr5T",
            "url": str(url)
        }
        result = requests.post(url=facepp_url, params=params, timeout=15)
        faces = json.loads(result.text)
        face_count = faces["face"]
        if len(face_count) > 0:
            return True
        else:
            return False
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
def face_detect(db_connection, db_cursor, id, photo_url):
    count = 0
    result = faceppAPI(photo_url)
    # 如果出错,则重新探查
    while result is None and count <= 5:
        result = faceppAPI(photo_url)
        count = count + 1
    else:
        # 没有出错,更改数据库
        if result is True:
            try:
                sql_command_update = "UPDATE photo SET f_hasface='TRUE' WHERE id={0}".format(id)
                db_cursor.execute(sql_command_update)
                db_connection.commit()
                print("Update success!")
            except Exception as e:
                db_connect().rollback()
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
    id, url = photo_detect(connection, cursor)
    while id is not None:
        try:
            face_detect(connection, cursor, id, url)
            id, url = photo_detect(connection, cursor)
        except Exception as e:
            print(e)
    close_connection(connection)


__main__()
