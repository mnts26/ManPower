#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django import http
from usiextensions.test.forms import *


def test_home(request):
    pageindex = 1
    form = TestingForm()
    form1 = TestingForm1()
    return render_to_response('test.html', locals(),
                              context_instance=RequestContext(request))