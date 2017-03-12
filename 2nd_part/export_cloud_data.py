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

# 读取所有数据
def select_data(connection, cursor):
    try:
        sql_command_select = "SELECT * FROM photo LIMIT 2;"
        #sql_command_select = "SELECT * FROM ms_emotion;"
        #sql_command_select = "SELECT * FROM facepp;"
        cursor.execute(sql_command_select)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        connection.rollback()

#写入全部的数据
def write_all_data():
    try:
        connection,cursor=db_connect()
        data_file=open('flickr_photos.txt','a')
        #data_file=open('me_emotion.txt','a')
        #data_file=open('facepp.txt','a')
        count=0
        for data in select_data(connection,cursor):
            count+=1
            if count%10000==0:
                print(count)
            writedata=""
            for x in data:
                writedata=str(writedata)+","+str(x)
            writedata=writedata+"\n"
            data_file.writelines(writedata)
    except Exception as e:
        print(e)

write_all_data()
