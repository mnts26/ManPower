#coding:utf-8
from django.contrib import admin
from base.models import *

class PartnerCategoryAdmin(admin.ModelAdmin):
    fieldsets = ((u'Ерөнхий', {'fields':('name','parent','description')}),)
    list_display = ('parent','name','description')
    search_fields = ('name','parent')
admin.site.register(PartnerCategory, PartnerCategoryAdmin)

class PartnerAdmin(admin.ModelAdmin):
    fieldsets = ((u'Ерөнхий', {'fields':('name','category_id')}),
                 (u'Нэмэлт', {'fields':('description','started_date',)}),
                 (u'Портал хандалт', {'fields':('user',)}))
    list_display = ('name','category_id','user')
    search_fields = ('name','category_id','user')
admin.site.register(Partner, PartnerAdmin)

class JobCategoryAdmin(admin.ModelAdmin):
    fieldsets = ((u'Ерөнхий', {'fields':('name','parent')}),
                 (u'Тайлбар', {'fields':('description',)}),)
    list_display = ('name','parent','description')
    search_fields = ('name','parent')
admin.site.register(JobCategory, JobCategoryAdmin)

