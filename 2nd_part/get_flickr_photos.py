# coding:utf-8
# version:python3.5.1
# author:kyh

import flickrapi
import psycopg2


# flickr照片类
class flickr_photo(object):
    def __init__(self, photo_id, photo_site, photo_url, photo_radius):
        self.id = photo_id
        self.site = photo_site
        self.url = photo_url
        self.radius = photo_radius

    # 将照片插入数据库
    def insert_db(self, db_cursor):
        try:
            sql_command_insert = "INSERT INTO photo(id,url,site,radius) " \
                                 "VALUES(" + self.id + ",'" + self.url + "','" + self.site + "','" + self.radius + ")"
            db_cursor.execute(sql_command_insert)
            site = db_cursor.fetchone()
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


# 查询需要挖掘数据的地点
def query_site(db_cursor):
    sql_command_select = "SELECT * " \
                         "FROM site " \
                         "WHERE start_query=='FALSE'"
    db_cursor.execute(sql_command_select)
    site = db_cursor.fetchone()
    if site is not None:
        site_name = site[1]
        lat = site[2][0]
        lon = site[2][1]
        sql_command_update = "UPDATE site " \
                             "SET start_query='FALSE' " \
                             "WHERE site_name=='" + str(site_name) + "'"
        return site, lat, lon
    else:
        return None


# flickr api信息
def flickrAPI():
    api_key = u'382e669299b2ea33fa2288fd7180326a'
    api_secret = u'b556d443c16be15e'
    flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=True)
    return flickr


# 计算时间
def compute_time(site, latitude, longitude, cursor, r=5):
    for year in list(range(2012, 2017)):
        for month in list(range(1, 13)):
            datemin = str(year) + "-" + str(month) + "-" + str("01")
            if month == 12:
                datemax = str(year + 1) + "-01-01"
            else:
                datemax = str(year) + "-" + str(month + 1) + "-" + str("01")
            get_photo_from_location(site, latitude, longitude, datemin, datemax, cursor, r=5)


# 获取照片
def get_photo_from_location(site, latitude, longitude, datemin, datemax, cursor, r=5):
    flickr = flickrAPI()
    try:
        # 获取所有图片
        photos = flickr.walk(lat=latitude, lon=longitude, radius=r,
                             min_taken_date=datemin, max_taken_date=datemax, per_page=500, extras='url_c')
    except Exception as e:
        print(e)
    # 获取每一张图片
    try:
        for photo_url in photos:
            url = photo_url.get('url_c')
            if url is not None:
                photo_id = photo_url.get('id')
                photo = flickr_photo(photo_id, site, url, r)
                if photo.insert_db(cursor):  # 插入数据库
                    print("Success! Photo id:" + id + "\tPhoto url:" + url)
    except Exception as e:
        print(e)


# 关闭数据库
def close_connection(db_cursor, site_name):
    try:
        sql_command_update = "UPDATE site " \
                             "SET end_query='FALSE' " \
                             "WHERE site_name=='" + str(site_name) + "'"
        print("Database Connection has been closed completely!")
        return True
    except Exception as e:
        print(e)


# 主操作步骤
db_connection, db_cursor = db_connect()
site, lat, lon = query_site(db_cursor)
if site is not None:
    compute_time(site, lat, lon, db_cursor, r=1)
    close_connection(db_cursor,site)
else:
    print("All sites have been recorded!")
