# coding:utf-8
# version:python3.5.1
# author:kyh

import psycopg2

# 表情类
class each_site(object):
    def __init__(self, site,date,count,happy_avg,happy_count,unhappy_count,sadness_average,neutral_average):
        self.site = site[:-7]
        self.date = date[:-3]
        self.count=count[0]
        self.happy_avg=happy_avg[0]
        self.happy=happy_count[0]
        self.unhappy=unhappy_count[0]
        self.sadness=sadness_average[0]
        self.neutral=neutral_average[0]

    def write_info(self, connection, cursor):
        try:
           file=open(self.site+".txt",'a')
           file.writelines("{0} {1} {2} {3} {4} {5} {6}\n".format(self.date,self.count,self.happy_avg,self.happy,self.unhappy,self.sadness,self.neutral))
           file.close()
        except Exception as e:
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


#获取数量信息
def get_count_info(connection,cursor,site,datemin,datemax):
    try:
        sql_command_select = "SELECT COUNT(*) FROM emotion WHERE photo_time>='{0}' and photo_time<'{1}' " \
                             "and site='{2}'".format(datemin,datemax,site)
        cursor.execute(sql_command_select)
        info_sum=cursor.fetchone()
    except Exception as e:
        print(e)
        cursor.rollback()
    try:
        sql_command_select = "SELECT Avg(happiness) FROM emotion WHERE photo_time>='{0}' and photo_time<'{1}' " \
                             "and site='{2}'".format(datemin,datemax,site)
        cursor.execute(sql_command_select)
        info_happy_avg=cursor.fetchone()
    except Exception as e:
        print(e)
        cursor.rollback()
    try:
        sql_command_select = "SELECT COUNT(*) FROM emotion WHERE photo_time>='{0}' and photo_time<'{1}' " \
                             "and site='{2}' and happiness>=0.5".format(datemin,datemax,site)
        cursor.execute(sql_command_select)
        info_happy=cursor.fetchone()
    except Exception as e:
        print(e)
        cursor.rollback()
    try:
        sql_command_select = "SELECT COUNT(*) FROM emotion WHERE photo_time>='{0}' and photo_time<'{1}' " \
                             "and site='{2}' and happiness<0.5".format(datemin,datemax,site)
        cursor.execute(sql_command_select)
        info_unhappy=cursor.fetchone()
    except Exception as e:
        print(e)
        cursor.rollback()
    try:
        sql_command_select = "SELECT AVG(sadness) FROM emotion WHERE photo_time>='{0}' and photo_time<'{1}' " \
                             "and site='{2}'".format(datemin,datemax,site)
        cursor.execute(sql_command_select)
        info_sadness=cursor.fetchone()
    except Exception as e:
        print(e)
        cursor.rollback()
    try:
        sql_command_select = "SELECT AVG(neutral) FROM emotion WHERE photo_time>='{0}' and photo_time<'{1}' " \
                             "and site='{2}'".format(datemin,datemax,site)
        cursor.execute(sql_command_select)
        info_neutral=cursor.fetchone()
    except Exception as e:
        print(e)
        cursor.rollback()
    site=each_site(site,datemin,info_sum,info_happy_avg,info_happy,info_unhappy,info_sadness,info_neutral)
    site.write_info(connection,cursor)

# 计算时间
def compute_time(connection,cursor,site):
    for year in list(range(2012, 2017)):
        for month in list(range(1, 13)):
            datemin = str(year) + "-" + str(month) + "-" + str("01")
            if month == 12:
                datemax = str(year + 1) + "-01-01"
            else:
                datemax = str(year) + "-" + str(month + 1) + "-" + str("01")
            if year==2016 and month == 7:
                break
            else:
                get_count_info(connection,cursor,site,datemin,datemax)


site='1LasVegasStripEmotion'
site='27MuseeDuLouvreEmotion'
site='52BigBenEmotion'
site='10ForbiddenCityEmotion'
site='13NotreDameCathedralEmotion'
site='2TimesSquareEmotion'
connection,cursor=db_connect()
compute_time(connection,cursor,site)
db_close(connection)
