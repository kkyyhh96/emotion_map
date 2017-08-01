# coding:utf-8
# version:python3.5.1
# author:kyh
# import flickr data which has geotags to csv
# useful


class flickr_data(object):
    def create_data_geotag(self, id, userid, photo_date_taken, photo_date_upload,
                           title, description, user_tags, longitude, latitude, accuracy, download_url):
        if longitude == 0:
            return None
        elif photo_date_taken == "null":
            flickr_str = "{0},'{1}',{2},'{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}'\n".format(id, userid,
                                                                                                   photo_date_taken,
                                                                                                   photo_date_upload,
                                                                                                   title, description,
                                                                                                   user_tags, longitude,
                                                                                                   latitude, accuracy,
                                                                                                   download_url)
            return flickr_str
        else:
            flickr_str = "{0},'{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}'\n".format(id, userid,
                                                                                                     photo_date_taken,
                                                                                                     photo_date_upload,
                                                                                                     title, description,
                                                                                                     user_tags,
                                                                                                     longitude,
                                                                                                     latitude, accuracy,
                                                                                                     download_url)
            return flickr_str

    def create_data(self, fileline):
        data = fileline.split('\t')
        for i in range(0, 23):
            if i == 3 or i == 4 or i == 10 or i == 11 or i == 12 or i == 17 or i == 18 or i == 22:
                if data[i] == "" or data[i] == 'null':
                    data[i] = 0
            if data[3] == 0:
                data[3] = "null"
        return self.create_data_geotag(data[0], data[1], data[3], data[4], data[6], data[7], data[8], data[10],
                                       data[11], data[12], data[13])


def __main__():
    # Parameter can be modified
    file_id = 4  # indicate which file to be imported
    once_push_count = 10000  # indicate how many lines will be imported in one time

    flickr_file = open("E:\BaiduNetdiskDownload\Flicker_geotag_library\AWS\yfcc100m_dataset-{0}".format(file_id), 'r')
    new_file = open("E:\BaiduNetdiskDownload\Flicker_geotag_library\AWS\yfcc100m_dataset-{0}-r.csv".format(file_id),
                    'a')
    line = flickr_file.readline()
    count = 1
    while line:
        data = flickr_data()
        wash_data = data.create_data(line)
        if wash_data is not None:
            new_file.write(wash_data)
        line = flickr_file.readline()
        count += 1
        if count % once_push_count == 0:
            print(count)
    flickr_file.close()
    new_file.close()


__main__()
