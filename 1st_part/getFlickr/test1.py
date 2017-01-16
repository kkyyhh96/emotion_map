import flickrapi

api_key=u'382e669299b2ea33fa2288fd7180326a'
api_secret=u'b556d443c16be15e'

flickr = flickrapi.FlickrAPI(api_key, api_secret,cache=True)
photos = flickr.photos.search(user_id='73509078@N00', per_page='10')
sets = flickr.photosets.getList(user_id='73509078@N00')
print("Hello World!")

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
sets   = flickr.photosets.getList(user_id='73509078@N00')
title  = sets['photosets']['photoset'][0]['title']['_content']
print('First set title: %s' % title)

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
raw_json = flickr.photosets.getList(user_id='73509078@N00',
                                    jsoncallback='foobar')
print(raw_json)
'''
flickr = flickrapi.FlickrAPI(api_key, api_secret)

(token, frob) = flickr.get_token_part_one(perms='write')
if not token: raw_input("Press ENTER after you authorized this program")
flickr.get_token_part_two((token, frob))

print('good')
flickr = flickrapi.FlickrAPI(api_key, api_secret,token=token)
flickr.authenticate_via_browser(perms='read')
'''