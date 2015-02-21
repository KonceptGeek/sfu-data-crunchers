from django.shortcuts import render_to_response
from django.template import RequestContext
import json
import os


def index(request):
    currentDir = os.path.dirname(os.path.realpath(__file__))
    joinedPath = os.path.join(currentDir,'../templates/assets/misc')
    print joinedPath

    context = RequestContext(request)
    with open(joinedPath+'/rent.json') as rentFile:
        rentJson = json.load(rentFile)

    with open(joinedPath+'/canada.geojson') as geoFile:
        geoJson = json.load(geoFile)

    rentJson = json.dumps(rentJson)
    geoJson = json.dumps(geoJson)
    contextDict = {'indexData': rentJson, 'geoJson': geoJson}
    return render_to_response('index.html', contextDict, context)