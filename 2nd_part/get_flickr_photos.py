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
    def insert_db(self, db_connection, db_cursor):
        try:
            sql_command_insert = "INSERT INTO photo(id,url,site,radius) " \
                                 "VALUES(" + str(self.id) + ",'" + self.url + "','" + self.site + "'," + str(
                self.radius) + ")"
            db_cursor.execute(sql_command_insert)
            db_connection.commit()
            return True
        except Exception as e:
            print(e)
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


# 查询需要挖掘数据的地点
def query_site(db_connection, db_cursor):
    sql_command_select = "SELECT * " \
                         "FROM site " \
                         "WHERE start_query='FALSE'"
    db_cursor.execute(sql_command_select)
    site = db_cursor.fetchone()
    # 如果存在这样的地点,记录经纬度进行挖掘
    if site is not None:
        site_name = site[1]
        lat = site[2].split(',')[0].split('(')[1]
        lon = site[2].split(',')[1].split(')')[0]
        sql_command_update = "UPDATE site " \
                             "SET start_query='TRUE' " \
                             "WHERE site_name='" + str(site_name) + "'"
        db_cursor.execute(sql_command_update)
        db_connection.commit()
        return site_name, lat, lon
    # 不存在这样的地点,说明已经全部挖掘完毕
    else:
        return None, None, None


# flickr api信息
def flickrAPI():
    api_key = u'382e669299b2ea33fa2288fd7180326a'
    api_secret = u'b556d443c16be15e'
    flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=True)
    return flickr


# 计算时间
def compute_time(db_connection, db_cursor, site, latitude, longitude, r=5):
    for year in list(range(2016, 2017)):
        for month in list(range(7, 13)):
            datemin = str(year) + "-" + str(month) + "-" + str("01")
            if month == 12:
                datemax = str(year + 1) + "-01-01"
            else:
                datemax = str(year) + "-" + str(month + 1) + "-" + str("01")
            get_photo_from_location(db_connection, db_cursor, site, latitude, longitude, datemin, datemax, r=5)


# 获取照片
def get_photo_from_location(db_connection, db_cursor, site, latitude, longitude, datemin, datemax, r=5):
    flickr = flickrAPI()
    # 获取所有图片
    try:
        photos = flickr.walk(lat=latitude, lon=longitude, radius=r,
                             min_taken_date=datemin, max_taken_date=datemax, per_page=500, extras='url_c')
    except Exception as e:
        print(e)
    # 获取每一张图片
    try:
        for photo_url in photos:
            url = photo_url.get('url_c')
            # 如果url不为空,将该图片插入数据库
            if url is not None:
                photo_id = int(photo_url.get('id'))
                photo = flickr_photo(photo_id, site, url, r)
                if photo.insert_db(db_connection, db_cursor):
                    print("Success! Photo id:" + id + "\tPhoto url:" + url)
    except Exception as e:
        print(e)


# 关闭数据库
def close_connection(connection, site_name):
    try:
        connection.close()
        print("Database Connection has been closed completely!")
        return True
    except Exception as e:
        print(e)


# 主操作步骤
def __main__():
    db_connection, db_cursor = db_connect()
    site, lat, lon = query_site(db_connection, db_cursor)
    if site is not None:
        compute_time(db_connection, db_cursor, site, lat, lon, r=1)
        close_connection(db_connection, site)
    else:
        print("All sites have been recorded!")


__main__()
