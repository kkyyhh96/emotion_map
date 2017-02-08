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


# 选择每一张人脸并获取其照片id
def select_data(connection, cursor):
    try:
        sql_command_select = "SELECT photo_id FROM ms_emotion WHERE start_join=FALSE limit 1;"
        cursor.execute(sql_command_select)
        data=cursor.fetchone()
        photo_id=str(data).split(',')[0].split('(')[1]
        sql_command_update="UPDATE ms_emotion SET start_join=TRUE WHERE photo_id={0}".format(photo_id)
        cursor.execute(sql_command_update)
        connection.commit()
        return photo_id
    except Exception as e:
        print(e)
        connection.rollback()
        return None


# 根据照片id获取具体信息
def update_data(connection, cursor, photo_id):
    try:
        # 获取具体信息
        sql_command_select = "SELECT coordinates,photo_take_date FROM photo WHERE id={0};".format(photo_id)
        print(sql_command_select)
        cursor.execute(sql_command_select)
        data = cursor.fetchone()
        print(data)

        x = str(data).split(',')[0].split('(')[2]
        y = str(data).split(',')[1].split(')')[0]
        date_year = str(data).split(',')[2].split('(')[1]
        date_month = str(data).split(',')[3].split(' ')[1]
        date_day = str(data).split(',')[4].split(')')[0].split(' ')[1]
        date = str(date_year) + "-" + str(date_month) + "-" + str(date_day)

        # 更新人脸信息
        sql_command_update = "UPDATE ms_emotion SET coordinates=point({0},{1}),photo_take_date='{2}',start_join=TRUE " \
                             "WHERE photo_id={3}".format(x, y, date, photo_id)
        cursor.execute(sql_command_update)
        print("Success!")
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()


def __main__():
    connection, cursor = db_connect()
    photo_id = select_data(connection, cursor)
    count=0
    while photo_id is not None:
        update_data(connection, cursor, photo_id)
        photo_id = select_data(connection, cursor)
        count+=1
        if count%2000==0:
            print(count)


__main__()
