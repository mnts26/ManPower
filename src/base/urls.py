from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'manpower.views.home', name='home'),
    # url(r'^manpower/', include('manpower.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
    url(r'^$', 'base.views.index'),
    url(r'^login$', 'base.views.login'),
    url(r'^logout$', 'base.views.logoutview'),
    url(r'^joblist/(?P<categ_id>.*)$', 'base.views.joblist'),
    url(r'^jobdetail/(?P<order_id>.*)$', 'base.views.jobdetail'),
    url(r'^jobform/(?P<order_id>.*)$', 'base.views.jobform'),
    url(r'^myjobs$', 'base.views.myjobs'),
    url(r'^addjobs$', 'base.views.addjob'),
    
    
)
