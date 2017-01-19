# coding:utf-8
# version:python3.5.1
# author:kyh

import flickrapi
import json
import re

# flickr api信息
def flickrAPI():
    api_key = u'382e669299b2ea33fa2288fd7180326a'
    api_secret = u'b556d443c16be15e'
    flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=True)
    return flickr

flickr = flickrAPI()
photo_id=31985743720
photo_info = flickr.photos.geo.getLocation(photo_id=photo_id, format='json')
print(photo_info)
photo_info=flickr.photos.getInfo(photo_id=photo_id,format='json')
print(photo_info.decode())
data=photo_info.decode()

dataj=json.loads(data)
print(dataj['photo']['dates']['posted'])

