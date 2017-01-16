# coding:utf-8
# version:python3.5.1
# author:kyh

import flickrapi

# flickr照片类
class flickr_photo(object):
    def __init__(self, photo_id, photo_site, photo_url, photo_radius):
        self.id = photo_id
        self.site = photo_site
        self.url = photo_url
        self.radius = photo_radius

    def insert_db(self):
        print(self.url)


# flickr api信息
def flickrAPI():
    api_key = u'382e669299b2ea33fa2288fd7180326a'
    api_secret = u'b556d443c16be15e'
    flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=True)
    return flickr


# 获取照片
def get_photo_from_location(site, latitude, longitude, datemin, datemax, r=0.5):
    flickr = flickrAPI()
    try:
        # 获取所有图片
        photos = flickr.walk(lat=latitude, lon=longitude, radius=r,
                             min_taken_date=datemin, max_taken_date=datemax, per_page=500, extras='url_c')
    except Exception as e:
        print(e)
    # 获取每一张图片
    try:
        for photo_url in photos:
            url = photo_url.get('url_c')
            if url is not None:
                photo_id = photo_url.get('id')
                print("Success! Photo id:" + id + "\nPhoto url:" + url)
                photo = flickr_photo(id, site, url)
                photo.insert_db()  # 插入数据库
    except Exception as e:
        print(e)


get_photo_from_location('5NiagaraFalls', 43.0828, -79.0742, '2015-06-02', '2015-06-03', 1)
get_photo_from_location('5NiagaraFalls', 43.0828, -79.0742, '2015-06-03', '2015-06-04', 1)
