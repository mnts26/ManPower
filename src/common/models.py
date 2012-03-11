#!coding=utf8
from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class CommonEducation(models.Model):
    name = models.CharField(u'Нэр', max_length=32)
    
    class Meta:
        verbose_name_plural = u"Боловсролууд"
        verbose_name = u"Боловсрол"

    def __unicode__(self):
        return self.name
    
class CommonCity(models.Model):
    name = models.CharField(u'Нэр', max_length=32)
    
    class Meta:
        verbose_name_plural = u"Аймаг хотууд"
        verbose_name = u"Аймаг хот"

    def __unicode__(self):
        return self.name

class CommonDistrict(models.Model):
    city = models.ForeignKey('CommonCity', verbose_name=u'Аймаг хот', related_name='district_set')
    name = models.CharField(u'Нэр', max_length=32)
    
    class Meta:
        verbose_name_plural = u"Сум дүүргүүд"
        verbose_name = u"Сум дүүрэг"

    def __unicode__(self):
        return self.name

class CommonSocialStatus(models.Model):
    name = models.CharField(u'Нэр', max_length=32)
    
    class Meta:
        verbose_name_plural = u"Нийгмийн гарлууд"
        verbose_name = u"Нийгмийн гарал"

    def __unicode__(self):
        return self.name

class CommonCountry(models.Model):
    name = models.CharField(u'Нэр', max_length=32)
    
    class Meta:
        verbose_name_plural = u"Улсууд"
        verbose_name = u"Улс"

    def __unicode__(self):
        return self.name

class CommonLanguage(models.Model):
    name = models.CharField(u'Нэр', max_length=32)
    
    class Meta:
        verbose_name_plural = u"Хэлүүд"
        verbose_name = u"Хэл"

    def __unicode__(self):
        return self.name
