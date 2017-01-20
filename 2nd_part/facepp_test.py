# coding:utf-8
# version:python3.5.1
# author:kyh

import requests

params = dict(api_key='iExD00qRzPaOm9lSFKhLMuKq-fVrs9pW',api_secret='B6_36b807WxgYLOTgjP94sc_QanKp-9T',image_url='https://farm9.staticflickr.com/8079/8386144607_effb3ca1df_c.jpg')
r = requests.post(url="https://api-cn.faceplusplus.com/facepp/v3/detect", params=params)
print(r.text)
