import json

import requests


def face_detect():
    try:
        params = {
            "api_key": "dab8719d9d8b3796a8689b861cfd3b36",
            "api_secret": "ollAKG4yNdTww_Zb9vcDiiOs7HHqxtZq",
            "url": "https://farm3.staticflickr.com/2873/8789347866_df9bf77620_c.jpg"
        }
        facepp_url = 'http://apicn.faceplusplus.com/v2/detection/detect'
        result = requests.post(url=facepp_url, params=params, timeout=15)
        faces = json.loads(result.text)
        face_count = faces["face"]
        if len(face_count) > 0:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return None

print(face_detect())
