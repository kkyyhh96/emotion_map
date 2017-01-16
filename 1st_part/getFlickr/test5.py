import flickrapi

api_key=u'382e669299b2ea33fa2288fd7180326a'
api_secret=u'b556d443c16be15e'

flickr = flickrapi.FlickrAPI(api_key, api_secret,cache=True)
try:
    photos = flickr.walk(geo_context='2',extras='url_c')
    #photos = flickr.walk(lat='30.54062',lon='114.375803',radius='30',extras='url_c')
except Exception:
    print('error')

for photo in photos:
    url=photo.get('url_c')
    if url is not None:
        print(url)
    else:
        print('url none')