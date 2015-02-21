from django.shortcuts import render_to_response
from django.template import RequestContext
import json.read


def index(request):
    context = RequestContext(request)
    contextDict = {'testData': json.read(open("rent.json"))}
    return render_to_response('index.html', contextDict, context)