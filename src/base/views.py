#!coding=utf8
# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext

def index(request):
    
    return render_to_response('index.html', locals(), 
                              context_instance=RequestContext(request))