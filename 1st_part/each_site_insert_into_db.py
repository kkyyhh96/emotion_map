# coding:utf-8
# version:python3.5.1
# author:kyh

import os

import psycopg2


# 表情类
class face_emotion(object):
    def __init__(self, site, url, date, anger, contempt, disgust, fear, happiness, neutral, sadness, surprise):
        self.site = site
        self.url = url
        self.date = date+"-01"
        self.anger = anger
        self.contempt = contempt
        self.disgust = disgust
        self.fear = fear
        self.happiness = happiness
        self.neutral = neutral
        self.sadness = sadness
        self.surprise = surprise

    def insert_emotion(self, connection, cursor):
        try:
            sql_command_update = "INSERT INTO emotion(site,url,photo_time,anger,contempt,disgust,fear,happiness,neutral," \
                                 "sadness,surprise) VALUES('{0}','{1}','{2}',{3},{4},{5},{6},{7},{8},{9},{10});".format(
                self.site,self.url,
                self.date, self.anger, self.contempt, self.disgust, self.fear, self.happiness, self.neutral,
                self.sadness, self.surprise)
            cursor.execute(sql_command_update)
            connection.commit()
            # print("Insert into database successfully!")
            return True
        except Exception as e:
            connection.rollback()
            print(e)


# 连接数据库
def db_connect():
    try:
        connection = psycopg2.connect(database="SweatMap", user="postgres",
                                      password="postgres", host="127.0.0.1", port="5432")
        cursor = connection.cursor()
        print("Database connection has been opened completely!")
        return connection, cursor
    except Exception as e:
        print(e)


# 关闭数据库
def db_close(connection):
    try:
        connection.close()
        print("Database connection has been closed completely!")
        return True
    except Exception as e:
        print(e)


# 遍历文件夹下的所有文件
def dir_walk(path, connection, cursor):
    for path_name, dir_names, file_names in os.walk(path):
        for file_name in file_names:
            try:
                print("Open file:{0}".format(file_name))
                site = open(path + '\\' + file_name, 'r')
                faces = site.readlines()
                for face in faces:
                    face_site = file_name.split('.')[0]
                    face_url = face.split(',')[0]
                    face_date = face.split(',')[1]
                    face_anger = face.split(',')[2]
                    face_contempt = face.split(',')[3]
                    face_disgust = face.split(',')[4]
                    face_fear = face.split(',')[5]
                    face_happiness = face.split(',')[6]
                    face_neutral = face.split(',')[7]
                    face_sadness = face.split(',')[8]
                    face_surprise = face.split(',')[9].split('\n')[0]
                    emotion = face_emotion(face_site, face_url, face_date, face_anger, face_contempt,
                                           face_disgust, face_fear, face_happiness, face_neutral,
                                           face_sadness, face_surprise)
                    emotion.insert_emotion(connection, cursor)
            except Exception as  e:
                print(e)


connection, cursor = db_connect()
dir_walk("E:\\Users\\KYH\\Documents\\KYH\\项目\\笑脸地图\\data\\essayData\\3Emotion", connection, cursor)
db_close(connection)
