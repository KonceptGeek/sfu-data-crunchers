from django.shortcuts import render_to_response
from django.template import RequestContext
import json


def index(request):
    context = RequestContext(request)
    with open('/Users/KonceptGeek/Documents/Projects/CODE2015/sfu-data-crunchers/YouthEmployment/youth_employment/rent.json') as rentFile:
        rentJson = json.load(rentFile)

    with open('/Users/KonceptGeek/Documents/Projects/CODE2015/sfu-data-crunchers/YouthEmployment/templates/assets/misc/canada.geojson') as geoFile:
        geoJson = json.load(geoFile)

    rentJson = json.dumps(rentJson)
    geoJson = json.dumps(geoJson)
    contextDict = {'indexData': rentJson, 'geoJson': geoJson}
    return render_to_response('index.html', contextDict, context)