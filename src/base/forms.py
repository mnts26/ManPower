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
#from captcha.fields import CaptchaField, JavaChallengeField
#from django.utils.translation import ugettext_lazy as _
import re

class JobCvForm(extForms.extModelForm) :
#    username        = forms.RegexField(label=_("Username"), max_length=30, regex=r'^\w+$',
#        help_text = _("Required. 30 characters or fewer. Alphanumeric characters only (letters, digits and underscores)."),
#        error_message = _("This value must contain only letters, numbers and underscores."))
#    password1       = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
#    password2       = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput)
#    email           = forms.EmailField(required=True)
#    last_name       = forms.CharField(required=True)
#    first_name      = forms.CharField(required=True)
#    family_name     = forms.CharField(required=True)
    #gender          = forms.
#    location        = extForms.extModelChoiceField(label=_("Location"), model=Location, 
#                search='name', display=('name','code'), required=True)
#    nullBoolean     = forms.NullBooleanField(label=_('Tiimuu'), required=True)
#    datetimer       = forms.DateTimeField(label=_('DateTime'), required=True)
#    date            = forms.DateField(label=_('Date'))
#    time            = forms.TimeField(label=_('Time'))
#    captcha         = CaptchaField(label=_('Confirmation code'), required=True)
#    challenge       = JavaChallengeField(label=_('Output of the following :'), required=True)
    
#    def clean_username(self) :
#        username = self.cleaned_data["username"]
#        try :
#            User.objects.get(username=username)
#        except User.DoesNotExist :
#            return username
#        raise forms.ValidationError(_("A user with that username already exists."))
#
#    def clean_password2(self) :
#        password1 = self.cleaned_data.get("password1", "")
#        password2 = self.cleaned_data["password2"]
#        if password1 != password2:
#            raise forms.ValidationError(_("The two password fields didn't match."))
#        return password2
#
#    def save(self, commit=True) :
#        user = super(MemberRegisterForm, self).save(commit=False)
#        user.set_password(self.cleaned_data["password1"])
#        if commit:
#            user.save()
#        return user
    
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