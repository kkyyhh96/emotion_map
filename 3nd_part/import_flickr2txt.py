# coding:utf-8
# version:python3.5.1
# author:kyh
# import each flickr data to database
import psycopg2


class flickr_data(object):
    def create_data(self, fileline):
        data = fileline.split('\t')
        txt_line = ''
        for i in range(0, 23):
            if i == 3 or i == 4 or i == 10 or i == 11 or i == 12 or i == 17 or i == 18 or i == 22:
                if data[i] == "" or data[i] == 'null':
                    data[i] = 0
            if i == 0 or i == 4 or i == 10 or i == 11 or i == 12 or i == 17 or i == 18:
                txt_line += str(data[i]) + ","
            elif i == 22:
                txt_line += str(data[i]).split('\n')[0]
            else:
                txt_line += "'" + str(data[i]) + "',"
        txt_line+="\n"
        return txt_line


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
def insert_data(connection, cursor, sql_command, count):
    try:
        cursor.execute(sql_command)
        connection.commit()
    except Exception as e:
        write_log(str(e), 1, count)
        connection.rollback()


def write_log(log, fileid, count):
    log_file = open("E:\BaiduNetdiskDownload\Flicker_geotag_library\AWS\log{0}.txt".format(fileid), 'a')
    log_file.writelines(str(count) + "\n" + str(log))
    log_file.close()


def __main__():
    # Parameter
    file_id = 1  # indicate which file to be imported
    once_push_count = 10000  # indicate how many lines will be imported in one time

    # Connect database
    con, cur = db_connect()

    # Open file
    flickr_file = open("E:\BaiduNetdiskDownload\Flicker_geotag_library\AWS\yfcc100m_dataset-{0}".format(file_id), 'r')
    txt_file = open("E:\BaiduNetdiskDownload\Flicker_geotag_library\AWS\yfcc100m_dataset-{0}-r.txt".format(file_id),
                    'a')
    count = 0
    txt_line = ""
    line = flickr_file.readline()
    while line:
        count += 1
        # write data
        data = flickr_data()
        txt_line += data.create_data(line)
        if count % once_push_count == 0:
            txt_file.write(txt_line)
            print(count)  # indicate how many data has been imported
            txt_line = ""
            # break
        line = flickr_file.readline()
    flickr_file.close()
    txt_file.close()


__main__()
