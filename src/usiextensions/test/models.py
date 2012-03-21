#coding:utf-8
"""
@copyright: Jacara
@contact: baskhuujacara@gmail.com; baskhuu@usi.mn
@summary: models of Testing usi extentions
"""
from django.db import models
from django.db.models import Q
import decimal


class TestingFields(models.Model) :
    name        = models.CharField(u'Текст талбар', max_length=100)
    date        = models.DateField(u"Огноо талбар")
    minitext    = models.CharField(u'Богино хэмжээний текст', max_length=10)
    password    = models.CharField(u'Нууц үг', max_length=10)
    text        = models.TextField(u'Том хэмжээний текст', null=True, blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]
        verbose_name_plural = u"Testing fields.."
        verbose_name = u"Testing fields.."

class TestingItem(models.Model):
    name        = models.CharField(u'Нэр', max_length=50)
    email       = models.EmailField(u'Мэйл хаяг', null=True, blank=True)
    
    class Meta :
        ordering = ["name"]
        verbose_name = u"Тест өгөгдөл"
        verbose_name_plural = u"select option ийг flexbox болгон ашиглах өгөгдлүүд"
