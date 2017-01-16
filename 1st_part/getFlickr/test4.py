import flickrapi

api_key=u'382e669299b2ea33fa2288fd7180326a'
api_secret=u'b556d443c16be15e'

flickr = flickrapi.FlickrAPI(api_key, api_secret,cache=True)

photos = flickr.photos.search(lat='31', lon='114', radius='30',extra='url_z')

for photo in photos[0]:
    print(photo.attrib['owner'])
    photoLoc = flickr.photos.geo.getLocation(photo_id=photo.attrib['id'])

    lat = photoLoc[0][0].attrib['latitude']
    lon = photoLoc[0][0].attrib['longitude']
    print (lat, lon)
    myurl=photo.get('url_z')
    print(myurl)