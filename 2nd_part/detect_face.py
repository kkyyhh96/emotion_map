# coding:utf-8
# version:python2.7.12
# author:kyh

from facepp import API

# face++的人脸
class facepp_face():
    def __init__(self, photo_id, site, gender, age, race, smile, glass):
        self.photo_id = photo_id
        self.site = site
        self.gender = gender
        self.age = age
        self.race = race
        self.smile = smile
        self.glass = glass

    def input_face(self):
        print "hello"


# face++API
def faceppAPI():
    api_key = '14d6d4c65fe5d7739db529369110b5ca'
    api_secret = 's5u3SLNzD5lCMyHioXKFOvsYx-jCl4Wl'
    api = API(api_key, api_secret)
    return api

#查询没被检测过人脸的照片
def photo_detect():
    print "hello"
# 探测人脸
def face_detect(photo_url):
    api = faceppAPI()
    face_info = api.detection.detect(url=photo_url)
    length=len(face_info['face'])
    face = facepp_face()
