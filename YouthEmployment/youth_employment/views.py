from django.shortcuts import render_to_response
from django.template import RequestContext
import json


def index(request):
    context = RequestContext(request)
    with open('/Users/KonceptGeek/Documents/Projects/CODE2015/sfu-data-crunchers/YouthEmployment/youth_employment/rent.json') as rentFile:
        rentJson = json.load(rentFile)
    rentJson = json.dumps(rentJson)
    contextDict = {'indexData': rentJson}
    return render_to_response('index.html', contextDict, context)