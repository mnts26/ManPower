#coding:utf-8
"""
@copyright: Jacara
@contact: baskhuujacara@gmail.com; baskhuu@usi.mn
@summary: forms of Testing usi extentions
"""
from django import forms
from usiextensions.viewtools import forms as extForms
from usiextensions.test.models import *
#import datetime

class TestingForm(extForms.extModelForm) :
    password     = extForms.extCharField(label=u"Нууц үг", widget=extForms.extPasswordInput)
    
    class Meta:
        model = TestingFields

class TestingForm1(forms.ModelForm):
    password     = forms.CharField(label=u"Нууц үг", widget=forms.PasswordInput)
    
    class Meta:
        model = TestingFields