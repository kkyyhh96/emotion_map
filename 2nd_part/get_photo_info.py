# coding:utf-8
# version:python3.5.1
# author:kyh

import flickrapi
import psycopg2


# 图片经纬度信息类
class photo_coordinates():
    def __init__(self, photo_id, photo_owner, photo_lat, photo_lon, photo_accuracy):
        self.photo_id = photo_id
        self.photo_owner = photo_owner
        self.photo_lat = photo_lat
        self.photo_lon = photo_lon
        self.photo_accuracy = photo_accuracy

    # 输入经纬度等信息
    def input_coordinates(self, connection, cursor):
        try:
            sql_command_update = "UPDATE photo " \
                                 "SET owner= WHERE"
            cursor.execute(sql_command_update)
            connection.commit()
            return True
        except Exception as e:
            print(e)
            return False


# 连接数据库
def db_connect():
    connection = psycopg2.connect(database="EmotionMap", user="postgres",
                                  password="postgres", host="127.0.0.1", port="5432")
    cursor = connection.cursor()
    return connection, cursor


# 查询需要补充信息的照片
def query_photo(db_cursor):
    sql_command_select = "SELECT * " \
                         "FROM photo " \
                         "WHERE start_info=='FALSE'"
    db_cursor.execute(sql_command_select)
    photo = db_cursor.fetchone()
    if photo is not None:
        photo_id = photo[0]
        sql_command_update = "UPDATE site " \
                             "SET start_info='TRUE' " \
                             "WHERE id=='" + str(photo_id) + "'"
        return photo_id
    else:
        return None


# flickr api信息
def flickrAPI():
    api_key = u'382e669299b2ea33fa2288fd7180326a'
    api_secret = u'b556d443c16be15e'
    flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=True)
    return flickr


# 获取图片的经纬度坐标等信息
def get_photo_coordinates(photo_id):
    flickr = flickrAPI()
    photo_info = flickr.photos.geo.getLocation(photo_id=photo_id, format='json')
    # 解析结果
    photo_owner = photo_info[1]
    photo_lat = photo_info[2]
    photo_lon = photo_info[3]
    photo_accuracy = photo_info[4]
    # 将信息录入数据库
    coordinates = photo_coordinates(photo_id, photo_owner, photo_lat, photo_lon, photo_accuracy)
    return coordinates.input_coordinates()


# 主要步骤
def __main__():
    connection, cursor = db_connect()
    photo = query_photo(cursor)
    while photo is not None:
        try:
            get_photo_coordinates(photo)
            photo = query_photo(cursor)
        except Exception as  e:
            print(e)
    print("All photos have information!")


__main__()
