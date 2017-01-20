# coding:utf-8
# version:python2.7.12
# author:kyh

from facepp import API
import psycopg2


# face++的人脸
class facepp_face():
    def __init__(self, photo_id, site, gender, age, race, smile, glass):
        self.photo_id = photo_id
        self.site = site
        self.gender = gender
        self.age = age
        self.race = race
        self.smile = smile
        self.glass = glass

    def input_face(self):
        print "hello"


# 连接数据库
def db_connect():
    connection = psycopg2.connect(database="EmotionMap", user="postgres",
                                  password="postgres", host="127.0.0.1", port="5432")
    cursor = connection.cursor()
    return connection, cursor


# face++API
def faceppAPI():
    api_key = 'cRe00o7bQIKV1DnOGK8yX_KAhkB9_aKH'
    api_secret = 'NOMOGO6OH0Z6xP5tbf9IBo2ldE'
    api = API(api_key, api_secret)
    return api


# 查询没被检测过人脸的照片
def photo_detect(db_connection, db_cursor):
    sql_command_select = "SELECT id,url FROM photo WHERE start_detect=FALSE LIMIT 1"
    db_cursor.execute(sql_command_select)
    photo = db_cursor.fetchone()
    if photo is not None:
        photo_id=photo[0]
        photo_url=photo[1]
        try:
            sql_command_update = "UPDATE photo SET start_detect='TRUE' WHERE id={0}".format(photo_id)
            db_cursor.execute(sql_command_update)
            db_connection.commit()
            return photo_id,photo_url
        except Exception as e:
            print e
            db_connection.rollback()
            return None,None
    else:
        return None,None

# 探测人脸
def face_detect(photo_url):
    api = faceppAPI()
    face_info = api.detection.detect(url=photo_url)
    print face_info
    length = len(face_info['face'])
    face = facepp_face()



def __main__():
    connection, cursor = db_connect()
    id,url=photo_detect(connection, cursor)
    face_detect(url)

__main__()
