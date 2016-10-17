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
    def __init__(self, _lat, _lng, _tags):
        self.lat = _lat
        self.lng = _lng
        self.tags = _tags

    def toJSON(self):
        return json.dumps(self.__dict__)


def loaddata():
    es = ESConnection.getESConnection()
    query = Search(index='t1').using(es).filter('range', timestamp_ms={'gte': 'now-5d', 'lt': 'now'})
    res = query.execute()
    print res.hits.total
    data = []
    for hit in res:
        lng = hit['coordinates'][0]
        lat = hit['coordinates'][1]
        text = hit['text']
        print lat,', ', lng
        data.append(poi(lat, lng, text.lower().split(' ')))
    return data


def index(request):
    return render_to_response('index.html')


def search(request):
    if 'keyword' in request.GET and request.GET['keyword']:
        keyword = request.GET['keyword']
    else:
        return render_to_response('')
    List = loaddata()
    poi_list = []
    for item in List:
        if keyword in item.tags:
            poi_list = poi_list + [item.toJSON()]

    result = json.dumps(poi_list)
    print result
    # return HttpResponse({'poi_list': poi_list}, content_type='application/json')
    # return render_to_response("result.html", {'poi_list': poi_list})
    return HttpResponse(result, content_type='application/json')


def search1(request):
    List = loaddata()
    poi_list = []
    count = 1

    render_to_response("result.html", {'poi_list': poi_list})
    while (1):
        poi_list += List[(count-1)*10:count*10]
        time.sleep(1)
        render_to_response("result.html", {'poi_list': poi_list})
