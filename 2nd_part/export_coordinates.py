# coding:utf-8
# version:python3.5.1
# author:kyh

import psycopg2


# 连接数据库
def db_connect():
    connection = psycopg2.connect(database="EmotionMap", user="postgres",
                                  password="postgres", host="127.0.0.1", port="5432")
    cursor = connection.cursor()
    return connection, cursor


def select_data(connection, cursor):
    try:
        sql_command_select = "SELECT coordinates from photos where coordinates is not null"
        cursor.execute(sql_command_select)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        connection.rollback()


connection, cursor = db_connect()
co_file=open('StockMapCoordinates.txt','a')
for data in select_data(connection,cursor):
    x=str(data).split(',')[0].split('(')[2]
    y=str(data).split(',')[1].split(')')[0]
    co_file.writelines(str(x)+","+str(y)+"\n")
co_file.close()
