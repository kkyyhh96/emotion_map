# coding:utf-8
# version:python3.5.1
# author:kyh

import flickrapi
import psycopg2
import json


# 图片经纬度信息类
class photo_coordinates():
    def __init__(self, photo_id, photo_owner, photo_post_date, photo_take_date, photo_lat, photo_lon, photo_accuracy):
        self.photo_id = photo_id
        self.photo_owner = photo_owner
        self.photo_upload = photo_post_date
        self.photo_take_date = photo_take_date
        self.photo_lat = photo_lat
        self.photo_lon = photo_lon
        self.photo_accuracy = photo_accuracy

    # 输入经纬度等信息
    def input_coordinates(self, connection, cursor):
        try:
            sql_command_update = "UPDATE photo SET owner='{0}',photo_upload={1},photo_take_date='{2}',coordinates=POINT({3},{4}),accuracy={5} WHERE id={6}".format(
                self.photo_owner, self.photo_upload, self.photo_take_date, self.photo_lat, self.photo_lon,
                self.photo_accuracy, self.photo_id)
            cursor.execute(sql_command_update)
            connection.commit()
            return True
        except Exception as e:
            print(e)
            connection.rollback()
            return False


# 连接数据库
def db_connect():
    connection = psycopg2.connect(database="EmotionMap", user="postgres",
                                  password="postgres", host="127.0.0.1", port="5432")
    cursor = connection.cursor()
    return connection, cursor


# 查询需要补充信息的照片
def query_photo(db_connection, db_cursor):
    sql_command_select = "SELECT id FROM photo WHERE start_info='FALSE' LIMIT 1"
    db_cursor.execute(sql_command_select)
    photo = db_cursor.fetchone()
    if photo is not None:
        photo_id = photo[0]
        try:
            sql_command_update = "UPDATE photo SET start_info='TRUE' WHERE id={0}".format(photo_id)
            db_cursor.execute(sql_command_update)
            db_connection.commit()
            return photo_id
        except Exception as e:
            print(e)
            db_connection.rollback()
            return None
    else:
        return None


# flickr api信息
def flickrAPI():
    api_key = u'382e669299b2ea33fa2288fd7180326a'
    api_secret = u'b556d443c16be15e'
    flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=True)
    return flickr


# 获取图片的经纬度坐标等信息
def get_photo_coordinates(connection, cursor, photo_id):
    flickr = flickrAPI()
    photo_info = flickr.photos.getInfo(photo_id=photo_id, format='json')
    photo_info = photo_info.decode()
    photo_info = json.loads(photo_info)
    # 解析结果
    try:
        photo_owner = photo_info["photo"]["owner"]["nsid"]
    except:
        photo_owner = ""
    try:
        photo_post_date = photo_info["photo"]["dates"]["posted"]
    except:
        photo_post_date = ""
    try:
        photo_take_date = photo_info["photo"]["dates"]["taken"]
    except:
        photo_take_date = ""
    try:
        photo_lat = photo_info["photo"]["location"]["latitude"]
    except:
        photo_lat = ""
    try:
        photo_lon = photo_info["photo"]["location"]["longitude"]
    except:
        photo_lon = ""
    try:
        photo_accuracy = photo_info["photo"]["location"]["accuracy"]
    except:
        photo_accuracy = ""
    # 将信息录入数据库
    coordinates = photo_coordinates(photo_id, photo_owner, photo_post_date, photo_take_date, photo_lat, photo_lon,
                                    photo_accuracy)
    return coordinates.input_coordinates(connection, cursor)


# 主要步骤
def __main__():
    connection, cursor = db_connect()
    photo = query_photo(connection, cursor)
    while photo is not None:
        try:
            get_photo_coordinates(connection, cursor, photo)
            photo = query_photo(connection, cursor)
        except Exception as  e:
            print(e)
    print("All photos have information!")


__main__()
