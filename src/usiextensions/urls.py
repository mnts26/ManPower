#coding:utf-8
"""
@author: Jacara
@summary: USI Extensions urls 
"""
from django.conf.urls.defaults import *

import os

urlpatterns = patterns('usiextensions.views',
                       (r'^forms/select/flexbox/(?P<model>.*)/(?P<search>.*)/(?P<display>.*)/', 'select_flexbox'),
)