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

connection,cursor=db_connect()
file = open('StockMapInfo.txt', 'r')
for data in file.readlines():
    photo_id = str(data).split(',')[0]
    lat = str(data).split(',')[1]
    lon = str(data).split(',')[2]
    year = str(data).split(',')[3]
    month = str(data).split(',')[4]
    day = str(data).split(',')[5]
    happy = str(data).split(',')[6]
    sad = str(data).split(',')[7]
    sql_command_insert = "INSERT INTO face(photo_id,coordinates,photo_time,happy,sad) VALUES({0},POINT({1},{2}),'{3}-{4}-{5}',{6},{7});".format(
        photo_id, lon, lat, year, month, day, happy, sad
    )
    try:
        cursor.execute(sql_command_insert)
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()
