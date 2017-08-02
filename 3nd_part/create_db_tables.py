# coding:utf-8
# version:python3.5.1
# author:kyh
# create tables and import data from csv to database tables
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


# Import data to each table
def import_data2table05():
    flickr_database = database()
    flickr_database.db_connect()
    # indicate which data should be imported into
    for file_id in range(0,6):
        print("Start {0}!".format(file_id))
        import_sql='''COPY flickr_geo{0} FROM
        'E:\BaiduNetdiskDownload\Flicker_geotag_library\AWS\yfcc100m_dataset-{0}-x.csv'
        '''.format(file_id)
        flickr_database.execute_sql(import_sql)
        print("End {0}!".format(file_id))

# Import data to each table
def import_data2table69():
    flickr_database = database()
    flickr_database.db_connect()
    # indicate which data should be imported into
    count=6
    for file_id in range(6,10):
        for file_id_s in range(0,5):
            print("Start {0}-{1}!".format(file_id,file_id_s))
            import_sql='''COPY flickr_geo{0} FROM
            'E:\BaiduNetdiskDownload\Flicker_geotag_library\AWS\yfcc100m_dataset-{1}-x-{2}.csv'
            '''.format(count,file_id,file_id_s)
            count+=1
            flickr_database.execute_sql(import_sql)
            print("End {0}!".format(file_id))


# Create tables
def create_tables05():
    # indicate how many tables should be created
    for file_id in range(0,6):
        create_table_sql='''CREATE TABLE flickr_geo{0}
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

# Create tables
def create_tables69():
    flickr_database = database()
    flickr_database.db_connect()
    count=6
    # indicate how many tables should be created
    for file_id in range(6,10):
        for file_id_s in range(0,5):
            create_table_sql='''CREATE TABLE flickr_geo{0}
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
    CREATE INDEX iflickr__geo_date{0} ON flickr_geo{0}(photo_date_taken);'''.format(count)
            count+=1
            flickr_database.execute_sql(create_table_sql)

#create_tables05()
create_tables69()
#import_data2table05()
#import_data2table69()

