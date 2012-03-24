# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import os
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'manpower.views.home', name='home'),
    # url(r'^manpower/', include('manpower.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('base.urls')),
    url(r'^base/', include('base.urls')),
    url(r'^common/', include('common.urls')),
    url(r'^ext/', include('usiextensions.urls')),
    
    (r'^extmedia/(?P<path>.*)$', 
                            'django.views.static.serve', 
                            {'document_root': os.path.join(os.path.dirname(__file__), 'usiextensions/media/'),
                            'show_indexes': True}),
    
    #url(r'^$', include('base.urls')),
    #url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    #        'document_root': settings.MEDIA_ROOT,
    #    }),
)
