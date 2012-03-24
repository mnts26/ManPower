#coding:utf-8
"""
@copyright: Jacara
@contact: baskhuujacara@gmail.com; baskhuu@usi.mn
@summary: forms of Android Site Base module
"""
from django import forms
from django.forms import ModelForm
from usiextensions import forms as extForms
from base.models import *
import datetime
#from captcha.fields import CaptchaField, JavaChallengeField
#from django.utils.translation import ugettext_lazy as _
import re

class JobCvForm(extForms.extModelForm) :
    birthcity = extForms.extModelChoiceField(label=u'Төрсөн аймаг, хот', model=CommonCity, 
                search='name', display=('name',))
    birthdistrict = extForms.extModelChoiceField(label=u'Төрсөн сум, дүүрэг', model=CommonDistrict, 
                search='name', display=('name','city__name'))
    education = extForms.extModelChoiceField(label=u'Боловсрол', model=CommonEducation, 
                search='name', display=('name',))
    socialstatus = extForms.extModelChoiceField(label=u'Нийгмийн гарал', model=CommonSocialStatus, 
                search='name', display=('name',))
    district = extForms.extModelChoiceField(label=u'Үндсэн захиргаа', model=CommonDistrict, 
                search='name', display=('name','city__name'))
    salary_request = extForms.extDecimalField(label=u'Цалингийн хүлээлт', widget=extForms.extDecimalWidget)
    
    class Meta:
        model = JobCv
        exclude = ['order','date_created']
#        sequence = [
#            (_('Basic Information'), ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']),
#            (_('Profile Information'), ['website','location','occupation','interest','signature']),
#            (_('Preferences'), ['show_email','hide_online','notify_reply','attach_signature', 'board_language'])
#        ]
    
#class MemberProfileForm(extForms.extModelForm):
#    last_name       = forms.CharField(label=_("Last name"), required=True)
#    first_name      = forms.CharField(label=_("First name"), required=True)
#    email           = forms.EmailField(label=_("E-Mail address"), required=True)
#    location        = extForms.extModelChoiceField(label=_("Location"), model=Location, 
#                search='name', display=('name','code'), required=True)
#    
#    def clean_username(self) :
#        username = self.cleaned_data["username"]
#        try :
#            User.objects.exclude(pk=self.instance.pk).get(username=username)
#        except User.DoesNotExist :
#            return username
#        raise forms.ValidationError(_("A user with that username already exists."))
#
#    def save(self, commit=True) :
#        user = super(MemberProfileForm, self).save(commit=False)
#        if commit:
#            user.save()
#        return user
#    
#    class Meta :
#        model = Member
#        exclude = ['password', 'is_active', 'is_superuser', 'last_login',
#                    'date_joined', 'groups', 'user_permissions', 'is_staff', 'board_style']
#        sequence = [
#            (_('Basic Information'),['username', 'first_name', 'last_name', 'email']),
#            (_('Profile Information'),['location', 'website','occupation','interest','signature']),
#            (_('Preferences'),['show_email','hide_online','notify_reply','attach_signature',
#                               'board_language'])
#        ]
#
#class NewsCommentForm(extForms.extModelForm) :
#    captcha         = CaptchaField(label=_('Are you a human?'), required=True)
#    comment         = extForms.extCharField(widget=extForms.extRichTextEditor(), required=True)
#    
#    class Meta :
#        model = NewsComment
#        exclude = ["news", "date"]
#        sequence = [
#            (_('Add comment'), ['commented_by','email','comment','captcha']),
#        ]
#
#class ToturialCommentForm(extForms.extModelForm) :
#    captcha         = CaptchaField(label=_('Are you a human?'), required=True)
#    comment         = extForms.extCharField(widget=extForms.extRichTextEditor(), required=True)
#    
#    class Meta :
#        model = ToturialComment
#        exclude = ["toturial", "date"]
#        sequence = [
#            (_('Add comment'), ['commented_by','email','comment','captcha']),
#        ]

class JobOrderForm(extForms.extModelForm) :
    category = extForms.extModelChoiceField(label=u'Ангилал', model=JobCategory, search='name', display=('parent__name','name',))
    level =  extForms.extModelChoiceField(label=u'Зэрэглэл', model=JobLevel, search='name', display=('name',))
    partner = forms.CharField(widget=forms.HiddenInput(), label='Байгууллага')
    
    def clean_partner(self):
        data = self.cleaned_data
        try:
            Partner.objects.get(username = data['partner'])
        except User.DoesNotExist:
            return data['partner']
        raise forms.ValidationError('This partner is already taken.')
    def save(self, user, *args, **kwargs):
        self.instance.partner = user             
        self.instance.create_date = datetime.date.today()              
        post = super(JobOrderForm, self).save(*args, **kwargs)
        post.save()
        return post

    class Meta:
        model = JobOrder
        exclude = ['create_date']