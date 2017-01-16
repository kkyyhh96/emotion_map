# coding:utf-8
# version:python3.5.1
# author:kyh

import flickrapi

# 图片经纬度信息类
class photo_coordinates():
    def __init__(self, photo_id, photo_owner, photo_lat, photo_lon, photo_accuracy):
        self.photo_id = photo_id
        self.photo_owner = photo_owner
        self.photo_lat = photo_lat
        self.photo_lon = photo_lon
        self.photo_accuracy = photo_accuracy

    def input_coordinates(self):
        print("coordinate")

# flickr api信息
def flickrAPI():
    api_key = u'382e669299b2ea33fa2288fd7180326a'
    api_secret = u'b556d443c16be15e'
    flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=True)
    return flickr

#获取图片的经纬度坐标等信息
def get_photo_coordinates(photo_id):
    flickr = flickrAPI()
    photo_info = flickr.photos.geo.getLocation(photo_id=photo_id, format='json')
