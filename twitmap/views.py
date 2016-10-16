from django.shortcuts import render_to_response
from django.http import HttpResponse
import datetime

import json

import urllib
import urllib2
import re


class poi(object):
    def __init__(self, _lat, _lng, _tags):
        self.lat = _lat
        self.lng = _lng
        self.tags = _tags

    def toJSON(self):
        return json.dumps(self.__dict__)


def loaddata():
    poi_list = []
    data_file = open('data/data.json')
    lines = data_file.readlines()
    for line in lines:
        line = line.strip()
        entry = json.loads(line)
        lat = float(entry["latlng"][0])
        lng = float(entry["latlng"][1])
        tags = []
        for word in entry["name"].split(' '):
            if word == '':
                continue
            word = word.lower()
            tags = tags + [word]
            tmp_entry = poi(lat, lng, tags)
            poi_list = poi_list + [tmp_entry]

    return poi_list


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
            poi_list = poi_list + [item]
    return render_to_response("result.html", {'poi_list': poi_list})
