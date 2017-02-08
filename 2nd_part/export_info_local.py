# coding:utf-8
# version:python3.5.1
# author:kyh

import psycopg2


# 连接数据库
def db_connect():
    connection = psycopg2.connect(database="StockMap", user="postgres",
                                  password="postgres", host="127.0.0.1", port="5432")
    cursor = connection.cursor()
    return connection, cursor


def select_data(connection, cursor):
    try:
        sql_command_select = "SELECT photo_id,coordinates,photo_take_date,happiness,sadness FROM ms_emotion;"
        cursor.execute(sql_command_select)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        connection.rollback()


connection, cursor = db_connect()
co_file=open('StockMapInfo.txt','a')
for data in select_data(connection,cursor):
    try:
        photo_id=str(data).split(',')[0].split('(')[1]
        x=str(data).split(',')[1].split('(')[1]
        y=str(data).split(',')[2].split(')')[0]
        year=str(data).split(',')[3].split('(')[1]
        month=str(data).split(',')[4].split(' ')[1]
        day=str(data).split(',')[5].split(')')[0].split(' ')[1]
        happiness=str(data).split(',')[6]
        sadness=str(data).split(',')[7].split(')')[0]
    except Exception as e:
        continue
    co_file.writelines("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(photo_id,x,y,year,month,day,happiness,sadness))
co_file.close()
