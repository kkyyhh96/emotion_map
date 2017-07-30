# coding:utf-8
# version:python3.5.1
# author:kyh
# import each flickr data to database
import psycopg2


class flickr_data(object):
    def create_data(self, fileline):
        data = fileline.split('\t')
        sql_line = "("
        for i in range(0, 23):
            if i is 3 or i is 4 or i is 10 or i is 11 or i is 12 or i is 17 or i is 18 or i is 22:
                if data[i] is "":
                    data[i] = 0
            if i is not 22:
                sql_line += "'" + str(data[i]) + "',"
            elif i == 22:
                sql_line += str(data[i]).split('\n')[0]
        sql_line += "),"
        return sql_line


# Connect database, return connection and cursor
def db_connect():
    # '''
    connection = psycopg2.connect(database="Flickr", user="FlickrTest",
                                  password="flickr", host="127.0.0.1", port="5432")
    '''
    connection = psycopg2.connect(database="Flickr", user="postgres",
                                  password="postgres", host="127.0.0.1", port="5432")
    '''
    cursor = connection.cursor()
    return connection, cursor


# Import data to database
def insert_data(connection, cursor, sql_command):
    try:
        cursor.execute(sql_command)
        connection.commit()
    except Exception as e:
        write_log(str(e))
        connection.rollback()


def write_log(log):
    log_file = open("E:\BaiduNetdiskDownload\Flicker_geotag_library\AWS\log.txt", 'a')
    log_file.writelines(str(log))
    log_file.close()


def __main__():
    # Parameter
    file_id = 0  # indicate which file to be imported
    once_push_count = 10000  # indicate how many lines will be imported in one time

    # Connect database
    con, cur = db_connect()

    # Open file
    flickr_file = open("E:\BaiduNetdiskDownload\Flicker_geotag_library\AWS\yfcc100m_dataset-{0}".format(file_id), 'r')
    sql_command = "INSERT INTO flickr VALUES "
    count = 0
    line = flickr_file.readline()
    while line:
        count += 1
        # write data
        data = flickr_data()
        sql_command += data.create_data(line)
        if count % once_push_count == 0:
            sql_command = sql_command[0:-1]
            insert_data(con, cur, sql_command)
            sql_command = "INSERT INTO flickr VALUES "
            print(count)  # indicate how many data has been imported
        line = flickr_file.readline()
    flickr_file.close()


__main__()
