#coding:utf-8
from django.contrib import admin
from common.models import *

# Common Models
class CommonEducationAdmin(admin.ModelAdmin):
    fieldsets = ((u'Ерөнхий мэдээлэл', {'fields':('name',)}),)
    list_display = ('name',)
    search_fields = ('name',)
admin.site.register(CommonEducation, CommonEducationAdmin)

class CommonCityAdmin(admin.ModelAdmin):
    fieldsets = ((u'Ерөнхий мэдээлэл', {'fields':('name',)}),)
    list_display = ('name',)
    search_fields = ('name',)
admin.site.register(CommonCity, CommonCityAdmin)

class CommonDistrictAdmin(admin.ModelAdmin):
    fieldsets = ((u'Ерөнхий мэдээлэл', {'fields':('city','name',)}),)
    list_display = ('city','name',)
    search_fields = ('city','name',)
admin.site.register(CommonDistrict, CommonDistrictAdmin)

class CommonSocialStatusAdmin(admin.ModelAdmin):
    fieldsets = ((u'Ерөнхий мэдээлэл', {'fields':('name',)}),)
    list_display = ('name',)
    search_fields = ('name',)
admin.site.register(CommonSocialStatus, CommonSocialStatusAdmin)

class CommonCountryAdmin(admin.ModelAdmin):
    fieldsets = ((u'Ерөнхий мэдээлэл', {'fields':('name',)}),)
    list_display = ('name',)
    search_fields = ('name',)
admin.site.register(CommonCountry, CommonCountryAdmin)

class CommonLanguageAdmin(admin.ModelAdmin):
    fieldsets = ((u'Ерөнхий мэдээлэл', {'fields':('name',)}),)
    list_display = ('name',)
    search_fields = ('name',)
admin.site.register(CommonLanguage, CommonLanguageAdmin)