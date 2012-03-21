#coding:utf-8
"""
@author: Jacara
@summary: USI Extensions views 
"""
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.core import serializers
from django.utils import simplejson as json
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.query import QuerySet
from django.db.models import Q
from django.http import HttpResponse

def select_flexbox(request, model, search, display) :
    name = request.POST['q']
    page = int(request.POST['p'])
    rows = int(request.POST['s'])
    
    app_label, model = model.split('.')
    content_type = ContentType.objects.get(app_label=app_label, model=model)
    object_model = content_type.model_class()
    query = eval("Q(%s__istartswith='%s')" % (search, name))
    qs = object_model.objects.filter(query)
    
    totalCount = qs.count()
    offset = ((page-1) * rows)-1
    if offset < 0 : offset = 0
    elif offset > totalCount :
        offset = 0
        page = 1
    if page > 1 :
        endoffset = rows * page
    else :
        endoffset = rows
    
    qs = qs.order_by(search)[offset:endoffset]
    
    display = display.split(',')
    results = {}
    for dn in display :
        results[dn] = '----------'
    results['id'] = ''
    mySet = {"total": totalCount, "results":[results]}
    for item in qs :
        item_dict = {}
        for dn in display :
            item_dict[dn] = getattr(item, dn, '')
        item_dict['id'] = item.id
        mySet['results'].append(item_dict)
    
    data = json.dumps(mySet)        # getting data of search dialog and dumping json object
    return HttpResponse(data, mimetype="application/javascript")
    