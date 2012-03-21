#coding: utf-8
from django.contrib import admin
from usiextensions.test.models import *

class TestingItemAdmin(admin.ModelAdmin):
    fieldsets = ((u'Туршилтийн өгөгдөл', {
                        'fields': ('name','email')
    }),)
    list_display = ('id', 'name', 'email')
    search_fields = ('id', 'name')

admin.site.register(TestingItem, TestingItemAdmin)

class TestingFieldsAdmin(admin.ModelAdmin):
    fieldsets = ((u'Туршилтийн өгөгдөл', {
                        'fields': ('name','date','minitext','password','text')
    }),)
    list_display = ('id', 'name', 'password','date','minitext','text')
    search_fields = ('id', 'name')

admin.site.register(TestingFields, TestingFieldsAdmin)