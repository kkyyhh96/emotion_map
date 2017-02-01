import requests
import json


url='http://apicn.faceplusplus.com/v2/detection/detect'
params={
    "api_key":"57e3cb964799b20befbcd091d9e2de8a",
    "api_secret":"veAGbxG-Js0aKJtbuV1HNXrp6DwUNttS",
    "url":"https://farm3.staticflickr.com/2873/8789347866_df9bf77620_c.jpg"
}
r=requests.post(url=url,params=params)
print(r.text)
