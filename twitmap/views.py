from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
import ES.ESConnection as ESConnection
import ES.Config as Config
from elasticsearch_dsl import Search
# import datetime
import time

import json

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


def loaddata():
    es = ESConnection.getESConnection()
    query = Search(index='t1').using(es).filter('range', timestamp_ms={'gte': 'now-5h', 'lt': 'now'})
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
    keyword = keyword.lower()
    List = loaddata()
    poi_list = []
    for item in List:
        if keyword in item.txt.lower().split(' '):
            poi_list = poi_list + [item.toJSON()]

    result = json.dumps(poi_list)
    # print result
    # return HttpResponse({'poi_list': poi_list}, content_type='application/json')
    # return render_to_response("result.html", {'poi_list': poi_list})
    return HttpResponse(result, content_type='application/json')
