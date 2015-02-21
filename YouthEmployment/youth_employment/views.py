from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
    context = RequestContext(request)
    contextDict = {'testData': {'test': 'bla'}}
    return render_to_response('index.html', contextDict, context)