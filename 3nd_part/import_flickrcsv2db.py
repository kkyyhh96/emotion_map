# coding:utf-8
# version:python3.5.1
# author:kyh
# import flickr data which has geotags to csv
import psycopg2


class database(object):
    # Connect database, return connection and cursor
    def db_connect(self):
        self.connection = psycopg2.connect(database="Flickr", user="FlickrTest",
                                           password="flickr", host="127.0.0.1", port="5432")
        self.cursor = self.connection.cursor()

    # Create table in database
    def execute_sql(self, sql):
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            with open("E:\BaiduNetdiskDownload\Flicker_geotag_library\AWS\log.txt", 'a') as f:
                f.writelines(str(e))
            self.connection.rollback()


# Import data to database
def insert_data(connection, cursor, sql_command):
    try:
        cursor.execute(sql_command)
        connection.commit()
    except Exception as e:
        with open("E:\BaiduNetdiskDownload\Flicker_geotag_library\AWS\log.txt", 'a') as f:
            f.writelines(str(e))
        connection.rollback()


def __main__():
    # Parameter can be modified
    file_id = 1  # indicate which file to be imported
    once_push_count = 10000  # indicate how many lines will be imported in one time

    create_table_sql = '''CREATE TABLE flickr_geo{0}
    (id BIGINT PRIMARY KEY NOT NULL,
    userid TEXT,
    photo_date_taken DATE,
    photo_date_uploaded BIGINT,
    title TEXT,
    description TEXT,
    user_tags TEXT,
    longitude FLOAT DEFAULT 0,
    latitude FLOAT DEFAULT 0,
    accuracy INTEGER DEFAULT 0,
    download_url TEXT NOT NULL
    );
    CREATE INDEX iflickr_geo_id{0} ON flickr_geo{0}(id);
    CREATE INDEX iflickr__geo_date{0} ON flickr_geo{0}(photo_date_taken);'''.format(file_id)

    flickr_database = database()
    flickr_database.db_connect()
    flickr_database.execute_sql(create_table_sql)

    flickr_file = open("E:\BaiduNetdiskDownload\Flicker_geotag_library\AWS\yfcc100m_dataset-{0}-r.csv".format(file_id),
                       'r')
    line = flickr_file.readline()
    count = 1
    sql_command_insert = "INSERT INTO flickr_geo{0} VALUES(".format(file_id)
    while line:
        sql_command_insert += "{0}),(".format(line)
        count += 1
        if count % once_push_count == 0:
            sql_command_insert = sql_command_insert[0:-2]
            flickr_database.execute_sql(sql_command_insert)
            sql_command_insert = "INSERT INTO flickr_geo{0} VALUES(".format(file_id)
            print(count)
        line=flickr_file.readline()
    sql_command_insert = sql_command_insert[0:-2]
    flickr_database.execute_sql(sql_command_insert)
    flickr_file.close()


__main__()
