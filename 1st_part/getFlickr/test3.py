import flickrapi

api_key=u'382e669299b2ea33fa2288fd7180326a'
api_secret=u'b556d443c16be15e'

flickr = flickrapi.FlickrAPI(api_key, api_secret,cache=True)
try:
    photos = flickr.walk(text='天安门',extras='url_z')
    photosGeo=flickr.photos.search(lat='30.54062',lon='114.375803',radius='300')
except Exception:
    print('error')
'''
for photo in photos:
    myurl=photo.get('url_z')
    #myurl = photo.get('url_z')
    if myurl is not None:
        print(myurl)
'''
for photo in photos:
    myurl=photo.get('url_z')
    if myurl is not None:
        print(myurl+"+lat:"+photos.attrib['latitude'])