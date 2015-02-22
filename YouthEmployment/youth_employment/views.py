from django.shortcuts import render_to_response
from django.template import RequestContext
import json
import os


def index(request):
    currentDir = os.path.dirname(os.path.realpath(__file__))
    joinedPath = os.path.join(currentDir,'../templates/assets/misc')

    context = RequestContext(request)
    with open(joinedPath+'/cleanData.json') as dataFile:
        cleanData = json.load(dataFile)

    with open(joinedPath+'/cities.geojson') as geoFile:
        geoJson = json.load(geoFile)

    with open(joinedPath+'/canada.geojson') as canadaGeoFile:
        canadaGeo = json.load(canadaGeoFile)

    cleanJson = json.dumps(cleanData)
    geoJson = json.dumps(geoJson)
    canadaJson = json.dumps(canadaGeo)
    contextDict = {'indexData': cleanJson, 'geoJson': geoJson, 'canadaJson': canadaJson}
    return render_to_response('index.html', contextDict, context)