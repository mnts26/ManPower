#!coding=utf8
from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class PartnerCategory(models.Model):
    name = models.CharField(u'Нэр', max_length=64)
    parent = models.ForeignKey('self', verbose_name=u'Эцэг ангилал', 
                related_name='child_set', blank=True, null=True)
    description = models.TextField(u'Тайлбар')
    
    class Meta:
        verbose_name_plural = u"Харилцагчийн ангилалууд"
        verbose_name = u"Харилцагчийн ангилал"

    def __unicode__(self):
        return self.name

class Partner(models.Model):
    name = models.CharField(u'Нэр', max_length=128)
    description = models.TextField(u'Тайлбар', blank=True, null=True)
    category_id = models.ForeignKey('PartnerCategory', verbose_name=u'Ангилал',
                related_name='partner_set')
    started_date = models.DateField(u'Байгуулагдсан он', blank=True, null=True)
    user = models.ForeignKey(User, verbose_name=u'Хандах эрх')
    
    class Meta:
        verbose_name_plural = u"Харилцагчид"
        verbose_name = u"Харилцагч"

    def __unicode__(self):
        return self.name

class JobCategory(models.Model):
    name = models.CharField(u'Нэр', max_length=128),
    description = models.TextField(u'Тайлбар', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = u"Ажлын ангилалууд"
        verbose_name = u"Ажлын ангилал"

    def __unicode__(self):
        return self.name

class JobLevel(models.Model):
    name = models.CharField(u'Нэр', max_length=128),
    description = models.TextField(u'Тайлбар', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = u"Ажлын зэрэглэлүүд"
        verbose_name = u"Ажлын зэрэглэл"

    def __unicode__(self):
        return self.name

class JobOrder(models.Model):
    category = models.ForeignKey('JobCategory', verbose_name=u'Ангилал', related_name='joborder_set'),
    level = models.ForeignKey('JobLevel', verbose_name=u'Зэрэглэл', related_name='joborder_set')
    name = models.CharField(u'Нэр', max_length=128),
    description = models.TextField(u'Тайлбар'),
    deadline = models.DateField(u'Эцсийн огноо', help_text=u'Хэрэв эцсийн огноо оруулахгүй бол уг ажлын байр байнга нээлттэй байх болно.'),
    active = models.BooleanField(u'Идэвхитэй', help_text=u'Уг ажлын байр ажил горилогчид харагдах эсэх')
    
    class Meta:
        verbose_name_plural = u"Ажлын байрууд"
        verbose_name = u"Ажлын байр"

    def __unicode__(self):
        return self.name

