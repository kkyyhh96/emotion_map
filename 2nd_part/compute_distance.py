# coding:utf-8
# version:python3.5.1
# author:kyh
import psycopg2


# 连接数据库
def db_connect():
    try:
        connection = psycopg2.connect(database="StockMap", user="postgres",
                                      password="postgres", host="127.0.0.1", port="5432")
        cursor = connection.cursor()
        print("Database connection has been opened completely!")
        return connection, cursor
    except Exception as e:
        print(e)

def select_coordinates(connection,cursor):
    try:
        sql_command_select="SELECT id,coordinates FROM face WHERE distance is null LIMIT 1 "
        cursor.execute(sql_command_select)
        data=cursor.fetchone()
        face_id=str(data).split(',')[0].split('(')[1]
        lon=str(data).split(',')[1].split('(')[1]
        lat=str(data).split(',')[2].split(')')[0]
        return face_id,lon,lat
    except Exception as e:
        print(e)
        return None,None,None

def compute_distance(cursor,lon,lat):
   try:
       sql_command_compute="SELECT st_distance(st_geomfromtext('point({0} {1})',4326),st_geomfromtext('point(-74.0095 40.7064)',4326),true)".format(lon,lat)
       cursor.execute(sql_command_compute)
       distance=cursor.fetchone()
       return distance
   except Exception as e:
       print(e)

def insert_db(connection,cursor,id,distance):
    try:
        distance=str(distance).split(',')[0].split('(')[1]
        sql_command_insert="UPDATE face SET distance={0} WHERE id={1}".format(distance,id)
        cursor.execute(sql_command_insert)
        connection.commit()
        return True
    except Exception as e:
        print(e)
        connection.rollback()

connection,cursor=db_connect()
id,lon,lat=select_coordinates(connection,cursor)
while id is not None:
    distance=compute_distance(cursor,lon,lat)
    insert_db(connection,cursor,id,distance)
    id,lon,lat=select_coordinates(connection,cursor)
