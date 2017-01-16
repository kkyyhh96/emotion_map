import flickrapi

# Information of Flickr API
def flickrAPI():
    api_key=u'382e669299b2ea33fa2288fd7180326a'
    api_secret=u'b556d443c16be15e'
    flickr = flickrapi.FlickrAPI(api_key, api_secret,cache=True)
    return flickr

#Get URL by key text
def getUrlFromText(string):
    flickr=flickrAPI()
    try:
        photos = flickr.walk(text=string,extras='url_c')
    except e:
        print('error!')

    url=getUrl(photos)
    return url

#Get URL by location which contains the latitude and the longitude of the center point with radius of searching round
def getUrlFromLocation(latitude,longitude,R=5):
    flickr=flickrAPI()
    try:
        photos = flickr.walk(lat=latitude,lon=longitude,radius=R,extras='url_c',min_taken_date="2012-4-01",max_taken_date="2012-4-30",per_page=500)
        print(R)
    except e:
        print('error!')

    url=getUrl(photos)
    return url

#Get URL by place name
def getUrlFromPlaceName(placeName):
    flickr=flickrAPI()
    #获取位置ID
    places=flickr.places.find(query=placeName)
    for place in places[0]:
        placeID=place.attrib['place_id']
        print(placeID)

    #爬取图片
    try:
        photos=flickr.walk(place_id=placeID,extras='url_c')
    except e:
        print('error!')

    url=getUrl(photos)

#Get URL exactly
def getUrl(photos):
    #遍历集合中的所有照片并获取URL
    count=0
    for photo in photos:
        url=photo.get('url_c')
        if url is not None:
            count+=1
            print(str(count)+"."+str(url))
        else:
            count+=1
            print(str(count)+'.url none')

#Set information here!
print('Start Downloading!')
# Input place name
#getUrlFromPlaceName('Wuhan University')
# Input key text
#getUrlFromText('Wuhan University')
# Input location
getUrlFromLocation(48.8584,2.2945,0.5)