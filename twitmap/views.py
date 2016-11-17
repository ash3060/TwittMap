from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
import ES.ESConnection as ESConnection
import ES.Config as Config
from elasticsearch_dsl import Search
# import datetime
import time

import json
from watson_developer_cloud import AlchemyLanguageV1

# import urllib
# import urllib2
# import re


class poi(object):
    def __init__(self, _lat, _lng, _usr, _txt):
        self.lat = _lat
        self.lng = _lng
        self.usr = _usr
        self.txt = _txt

    def toJSON(self):
        return json.dumps(self.__dict__)


def loaddata(hascenter, center=None, radius=None):
    # if (hascenter):
        # has center and radius
    # else:
        # don't have center and radius
    es = ESConnection.getESConnection()
    # print "connection cost: ", time.time()-mtime
    if (hascenter):
        query = Search(index='t1').using(es).filter('range', timestamp_ms={'gte': 'now-30m', 'lt': 'now'}).\
        filter({'geo_distance': {'distance':radius+"km",'coordinates':[float(center[1]), float(center[0])]}})
    else:
        query = Search(index='t1').using(es).filter('range', timestamp_ms={'gte': 'now-30m', 'lt': 'now'})

    # print "query cost: ", time.time()-mtime
    res = query.scan()
    #print res.hits.total
    data = []
    for hit in res:
        lat = hit['coordinates'][1]
        lng = hit['coordinates'][0]
        text = hit['text']
        usr = hit['username']
        # print lat,', ', lng
        data.append(poi(lat, lng, usr, text))
    return data


def index(request):
    return render_to_response('index.html')


def search(request):
    if 'keyword' in request.GET and request.GET['keyword']:
        keyword = request.GET['keyword']
    else:
        return render_to_response('')
    hascenter = False;
    if ('center' in request.GET and request.GET['center']
        and 'radius' in request.GET and request.GET['radius']):
        hascenter = True
        centerS = request.GET['center']  # 41.244772,-98.4375
        radius = request.GET['radius']
        index = centerS.find(',')
        center=[]
        center.append(float(centerS[:index]))
        center.append(float(centerS[index+1:]))
        print center
        print radius

    keyword = keyword.lower()
    if (hascenter):
        List = loaddata(True, center, radius)
    else:
        List = loaddata(False)

    alchemy_language = AlchemyLanguageV1(api_key='a3cb86812805b8f50074201572d8310c864081bd')

    poi_list = []
    for item in List:
        if keyword in item.txt.lower().split(' '):
            poi_list = poi_list + [item.toJSON()]
            sentRes = alchemy_language.sentiment(text=item.txt)
            # print item.txt
            # print sentRes['docSentiment']['type']
    # print "search keyword cost: ", time.time()-mtime
    result = json.dumps(poi_list)
    # print result
    # return HttpResponse({'poi_list': poi_list}, content_type='application/json')
    # return render_to_response("result.html", {'poi_list': poi_list})
    return HttpResponse(result, content_type='application/json')


def confirm(request):
    print json.dumps(request.POST)
