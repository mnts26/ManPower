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
                return HttpResponseRedirect('/base/myjobs')
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
    job_list = JobOrder.objects.filter(category__in=categ_ids,active=True).order_by('-create_date')
    return render_to_response('joblist.html', locals(), 
                              context_instance=RequestContext(request))

def jobdetail(request, order_id):
    order = JobOrder.objects.get(pk=order_id)
    job_name = order.name
    categ = order.category
    job_list = [order]
    partner = order.partner
    return render_to_response('joblist.html', locals(),
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
        PhoneFormSet = inlineformset_factory(JobCv, JobCvPhone, extra=5, max_num=5)
        phoneform = PhoneFormSet(instance=cv)
        OccupationFormSet = inlineformset_factory(JobCv, JobCvEducation, extra=5, max_num=8)
        occupationform = OccupationFormSet(instance=cv)
        CourseFormSet = inlineformset_factory(JobCv, JobCvCourse, extra=5, max_num=8)
        courseform = CourseFormSet(instance=cv)
        LanguageFormSet = inlineformset_factory(JobCv, JobCvForeignLanguage, extra=5, max_num=5)
        languageform = LanguageFormSet(instance=cv)
        SkillFormSet = inlineformset_factory(JobCv, JobCvSkill, extra=5, max_num=8)
        skillform = SkillFormSet(instance=cv)
        UsageFormSet = inlineformset_factory(JobCv, JobCvUsage, extra=5, max_num=8)
        usageform = UsageFormSet(instance=cv)
        WorkingFormSet = inlineformset_factory(JobCv, JobCvWorking, extra=5, max_num=5)
        workingform = WorkingFormSet(instance=cv)
        RelationFormSet = inlineformset_factory(JobCv, JobCvRelation, extra=5, max_num=5)
        relationform = RelationFormSet(instance=cv)
        return render_to_response('jobcvform.html', locals(),
                              context_instance=RequestContext(request))
        
@login_required        
def myjobs(request):
    partner = None
    partners = Partner.objects.filter(user__pk=request.user.pk)
    if partners:
        partner = partners[0]
        return render_to_response('myjobs.html', locals(),
                                  context_instance=RequestContext(request))
    else :
        print 'bhq'
        return HttpResponseRedirect('/')

@login_required
def addjob(request):
    partners = Partner.objects.filter(pk=request.user.pk)
    partner = partners[0]
    form = JobOrderForm()
    if request.POST:
        print '1'
        form = JobOrderForm(request.POST)
        if form.is_valid():
            print '3'
            form.save(user=request.user)
            print '4'
            return HttpResponseRedirect('/baitsaagch/dugnelt')
    else :
        return render_to_response('addjobs.html', locals(),
                              context_instance=RequestContext(request))
    