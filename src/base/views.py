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
    print 'categ_ids :', categ_ids
    job_list = JobOrder.objects.filter(category__in=categ_ids,active=True).order_by('-create_date')
    print 'job_list :', job_list
    return render_to_response('joblist.html', locals(), 
                              context_instance=RequestContext(request))

def jobdetail(request, order_id):
    
    order = JobOrder.objects.get(pk=order_id)
    partner = order.partner
    return render_to_response('jobdetail.html', locals(),
                              context_instance=RequestContext(request))