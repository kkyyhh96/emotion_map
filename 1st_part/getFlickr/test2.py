import flickrapi

api_key=u'382e669299b2ea33fa2288fd7180326a'
api_secret=u'b556d443c16be15e'

flickr = flickrapi.FlickrAPI(api_key, api_secret)

(token, frob) = flickr.get_token_part_one(perms='write')
if not token:
    raw_input("Press ENTER after you authorized this program")
print (token)

flickr.get_token_part_two((token, frob))

# 得到token 后就可以干自己想干的事
flickr = flickrapi.FlickrAPI(api_key, api_secret, token=token)

try:
    photos = flickr.walk(text='girl', tag_mode='all',
        tags='girl',
        min_upload_date='2014-02-05',
        max_upload_date='2014-02-06',
        extras='owner_name,tags,url_q,url_m,url_o')
except Exception:
    print( 'error')
    exit()

try:
    for photo in photos:
        print (photo.get('id'), photo.get('title'))
        print (photo.get('url_m'))
        print ("")

except ex:
    print (Exception,':',ex)