#coding:utf-8
from django.contrib import admin
from base.models import *

class PartnerCategoryAdmin(admin.ModelAdmin):
    fieldsets = ((u'Ерөнхий', {'fields':('name','parent','description')}),)
    list_display = ('parent','name','description')
    search_fields = ('name','parent')
admin.site.register(PartnerCategory, PartnerCategoryAdmin)

class PartnerAdmin(admin.ModelAdmin):
    fieldsets = ((u'Ерөнхий', {'fields':('name','category_id','poster','logo','website')}),
                 (u'Нэмэлт', {'fields':('description','started_date','level')}),
                 (u'Портал хандалт', {'fields':('user',)}))
    list_display = ('level','admin_image','name','category_id','user')
    search_fields = ('name','category_id','user')
    filter_fields = ('level',)
admin.site.register(Partner, PartnerAdmin)

class JobCategoryAdmin(admin.ModelAdmin):
    fieldsets = ((u'Ерөнхий', {'fields':('name','parent')}),
                 (u'Тайлбар', {'fields':('description',)}))
    list_display = ('name','parent','description')
    search_fields = ('name','parent')
admin.site.register(JobCategory, JobCategoryAdmin)

class JobOrderAdmin(admin.ModelAdmin):
    fieldsets = ((u'Ерөнхий мэдээлэл', {'fields':('category','partner','level','name')}),
                 (u'Бусад мэдээлэл', {'fields':('description','requirement','deadline','active')}))
    list_display = ('category','name','partner','level','deadline','active')
    search_fields = ('name','category','partner')
admin.site.register(JobOrder, JobOrderAdmin)

class JobLevelAdmin(admin.ModelAdmin):
    fieldsets = ((u'Ерөнхий', {'fields':('name',)}),
                 (u'Тайлбар', {'fields':('description',)}))
    list_display = ('name','description')
    search_fields = ('name',)
admin.site.register(JobLevel, JobLevelAdmin)

