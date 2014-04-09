import urllib2
import json

def get_name_from_API():

    sliver_info = []
    request = urllib2.Request('http://127.0.0.1/confine/api/node/')
    response= None
    try:
        response = urllib2.urlopen(request)
    except:
        response = None


    if(response is None):
        return None

    page = json.loads(response.read())
    return page['name']


print(get_name_from_API())