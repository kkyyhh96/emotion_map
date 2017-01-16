import flickrapi

api_key=u'382e669299b2ea33fa2288fd7180326a'
api_secret=u'b556d443c16be15e'
flickr = flickrapi.FlickrAPI(api_key, api_secret)

#获取位置ID
location=flickr.places.find(query='Wuhan University')

for local in location[0]:
    placeid=local.attrib['place_id']
    print(placeid+"\n"+local.attrib['latitude']+"\n"+local.attrib['longitude'])

try:
    photos = flickr.walk(place_id=placeid,extras='url_c')
except Exception:
    print('error')

for photo in photos:
    url=photo.get('url_c')
    if url is not None:
        print(url)
    else:
        print('url none')