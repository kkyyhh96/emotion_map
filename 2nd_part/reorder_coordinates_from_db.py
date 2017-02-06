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


def select_data(connection, cursor):
    try:
        sql_command_select = "SELECT x,y FROM coordinates ORDER BY x"
        cursor.execute(sql_command_select)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        connection.rollback()


connection, cursor = db_connect()
co_file = open('StockMapCoordinatesOrder.txt', 'a')
last_data_x = 0
last_data_y = 0
count = 1
for data in select_data(connection, cursor):
    x = data[0]
    y = data[1]
    if last_data_x == x and last_data_y == y:
        count += 1
    else:
        co_file.writelines('{0},{1},{2}\n'.format(last_data_x,last_data_y,count))
        count = 1
        last_data_x=x
        last_data_y=y
else:
    co_file.writelines('{0},{1},{2}\n'.format(last_data_x,last_data_y,count))
co_file.close()
