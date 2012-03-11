#!coding=utf8
# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from base.models import *
from common.models import *

def index(request):
    
    return render_to_response('index.html', locals(), 
                              context_instance=RequestContext(request))

def joblist(request, categ_id):
    
    categ = JobCategory.objects.get(id=categ_id)
    categ_ids = JobCategory.get_all_children(categ)
    job_ids = JobOrder.objects.filter(category__in=categ_ids)
    return render_to_response('joblist.html', locals(), 
                              context_instance=RequestContext(request))