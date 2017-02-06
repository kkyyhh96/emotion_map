# coding:utf-8
# version:python3.5.1
# author:kyh

import psycopg2


# 连接数据库
def db_connect():
    connection = psycopg2.connect(database="StockMap", user="postgres",
                                  password="postgres", host="127.0.0.1", port="5432")
    cursor = connection.cursor()
    print("Start!")
    return connection, cursor


def insert_data(connection, cursor, x, y):
    try:
        sql_command_insert = "insert into coordinates(x,y) values({0},{1})".format(x, y)
        cursor.execute(sql_command_insert)
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()


connection, cursor = db_connect()
co_file = open('StockMapCoordinates.txt', 'r')
lines = co_file.readlines()
co_file.close()
count=0
for line in lines:
    x = str(line).split(',')[0]
    y = str(line).split(',')[1].split('\n')[0]
    count+=1
    if count%10000==0:
        print(count)
    insert_data(connection, cursor, x, y)
