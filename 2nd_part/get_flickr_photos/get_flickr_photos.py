#coding:utf-8
#version:python3.5.1
#author:kyh

import flickrapi
import time
import psycopg2

#flickr照片类
class flickr_photo(object):
    def __init__(self,url, site,lat,lon,radius,date):
        self.site = site
        self.url =url
        self.lat = lat
        self.lon = lon
        self.radius = radius
        self.date = date

    def insert_db():
        print('1')

#flickr api信息
def flickrapi():
	api_key = u'382e669299b2ea33fa2288fd7180326a'
	api_secret = u'b556d443c16be15e'
	flickr = flickrapi.FlickrAPI(api_key, api_secret,cache=True)
	return flickr

#获取照片
def get_photo_from_location(site,latitude,longitude,datemin,datemax,r=5):
	flickr = flickrapi()
	print('0')
	try:
		#获取所有图片
		photos = flickr.walk(lat=latitude,lon=longitude,radius=r,
					 min_taken_date=datemin,max_taken_date=datemax,per_page=500,extras='url_c')
	except Exception as e:
		print(e)
	#获取每一张图片
	try:
		for photo_url in photos:
			url = photo.get('url_c')
			if url is not None:
				photo = flickr_photo(url,site,latitude,longitude,r,datemin)
				photo.insert_db()#插入数据库
	except Exception as e:
		print(e)

get_photo_from_location('5NiagaraFalls',43.0828,-79.0742,'2015-06-01','2015-06-30',1)

