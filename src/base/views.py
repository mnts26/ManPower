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
from base.models import *
from common.models import *
from base.forms import *
import smtplib


# PDF RENDER
import cStringIO as StringIO
#import ho.pisa as pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape

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
    full_content = True
    order = JobOrder.objects.get(pk=order_id)
    PhoneFormSet = inlineformset_factory(JobCv, JobCvPhone, extra=5, max_num=5, 
                                             form=JobCvPhoneForm, formset=PhoneInlineFormSet)
    OccupationFormSet = inlineformset_factory(JobCv, JobCvEducation, extra=5, max_num=5,
                                              form=JobCvEducationForm)
    CourseFormSet = inlineformset_factory(JobCv, JobCvCourse, extra=5, max_num=5,
                                          form=JobCvCourseForm)
    LanguageFormSet = inlineformset_factory(JobCv, JobCvForeignLanguage, extra=5, max_num=5,
                                            form=JobCvLanguageForm)
    SkillFormSet = inlineformset_factory(JobCv, JobCvSkill, extra=8, max_num=8,
                                         form=JobCvSkillForm)
    UsageFormSet = inlineformset_factory(JobCv, JobCvUsage, extra=8, max_num=8,
                                         form=JobCvUsageForm)
    WorkingFormSet = inlineformset_factory(JobCv, JobCvWorking, extra=5, max_num=5,
                                           form=JobCvWorkingForm)
    RelationFormSet = inlineformset_factory(JobCv, JobCvRelation, extra=5, max_num=5,
                                            form=JobCvRelationForm)
    if request.POST:
        cv = JobCv()
        form = JobCvForm(request.POST, request.FILES, instance=cv)
        phoneform = PhoneFormSet(request.POST, instance=cv)
        occupationform = OccupationFormSet(request.POST, instance=cv)
        courseform = CourseFormSet(request.POST, instance=cv)
        languageform = LanguageFormSet(request.POST, instance=cv)
        skillform = SkillFormSet(request.POST, instance=cv)
        usageform = UsageFormSet(request.POST, instance=cv)
        workingform = WorkingFormSet(request.POST, instance=cv)
        relationform = RelationFormSet(request.POST, instance=cv)
        if form.is_valid() and phoneform.is_valid() and occupationform.is_valid() and \
            courseform.is_valid() and languageform.is_valid() and skillform.is_valid() and \
            usageform.is_valid() and workingform.is_valid() and relationform.is_valid():
            
            cvobject = form.save()
            phoneform.save()
            occupationform.save()
            courseform.save()
            languageform.save()
            skillform.save()
            usageform.save()
            workingform.save()
            relationform.save()
            return HttpResponseRedirect('/base/jobdetail/%s' % order_id)
    else :
        cv = JobCv()
        form = JobCvForm(instance=cv)
        phoneform = PhoneFormSet(instance=cv)
        occupationform = OccupationFormSet(instance=cv)
        courseform = CourseFormSet(instance=cv)
        languageform = LanguageFormSet(instance=cv)
        skillform = SkillFormSet(instance=cv)
        usageform = UsageFormSet(instance=cv)
        workingform = WorkingFormSet(instance=cv)
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
def addjobs(request):
    partners = Partner.objects.filter(pk=request.user.pk)   
    partner = partners[0]
    form = JobOrderForm()
    if request.method == 'POST':
       form = JobOrderForm(request.POST)
       if form.is_valid():
           job = form.save(commit=False)
           job.partner = partner
           job.save()
           return HttpResponseRedirect('/base/addjobs')
    else :
        form = JobOrderForm()
    return render_to_response('new/addjobs.html', locals(),
                              context_instance=RequestContext(request))
def contactable (request):
    print 'ASDASDASDASDS'
    
def aboutus(request):
    print 'HALSDM<L:ASMD KA:LSM DKLASM '
    return render_to_response('new/aboutus.html', locals(),
                              context_instance=RequestContext(request))

def lessons(request):
    return render_to_response('new/lessons.html', locals(),
                              context_instance=RequestContext(request))
def jobs(request):
    return render_to_response('new/jobs.html', locals(),
                              context_instance=RequestContext(request))
def events(request):
    return render_to_response('new/events.html', locals(),
                              context_instance=RequestContext(request))

def partners (request):
    partners = Partner.objects.all()
    for partner in partners: 
        print "TEST" , partner.logo 
    return render_to_response('new/partners.html', locals(),
                              context_instance=RequestContext(request))
    
def sendmail (request):
    
    to = 'xac_tsolmon@yahoo.com'
    gmail_user = 'manpowermn@gmail.com'
    gmail_pwd ='gino_1203'
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Welcome to ManPower \n'
    print header
    msg = header + '\n this is test msg from manpower.mn \n\n'
    smtpserver.sendmail(gmail_user, to, msg)
    print 'done!'
    smtpserver.close()

def pdfview(request):
    results = "Some Text"
    return render_to_pdf(
            'new/pdf_template.html',
            {
                'pagesize':'A4',
                'mylist': results,
            }
        )

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
#    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
#    if not pdf.err:
#        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
        