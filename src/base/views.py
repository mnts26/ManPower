#!coding=utf8
# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from base.models import *
from common.models import *
from base.forms import *
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory


def index(request):
    
    return render_to_response('index.html', locals(), 
                              context_instance=RequestContext(request))
    
def login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                state = "You're successfully logged in!"
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."
    return render_to_response('index.html', locals(), 
                              context_instance=RequestContext(request))
@login_required
def logoutview(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/')
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

def jobform(request, order_id):
    order = JobOrder.objects.get(pk=order_id)
    if request.POST:
        JobCvFormset = inlineformset_factory(JobCv, JobCvPhone, extra=0)
        form = JobCvForm(request.POST)
        formset = JobCvFormset(request.POST)
        return HttpResponseRedirect('base/jobdetail/%s' % order_id)
    else :
        cv = JobCv()
        form = JobCvForm(instance=cv)
        JobCvFormset = inlineformset_factory(JobCv, JobCvPhone, extra=0)
        formset = JobCvFormset(instance=cv)
        return render_to_response('jobcvform.html', locals(),
                              context_instance=RequestContext(request))
        