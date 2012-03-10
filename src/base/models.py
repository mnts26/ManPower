from django.db import models

# Create your models here.

class PartnerCategory(models.Model):
    name = models.CharField(u'Нэр', max_length=64)
    parent = models.ForeignKey('self', verbose_name=u'Эцэг ангилал', 
                related_name='child_set', blank=True, required=False),
    descirption = models.TextField(u'Тайлбар')
    
    class Meta:
        verbose_name_plural = u"Харилцагчийн ангилалууд"
        verbose_name = u"Харилцагчийн ангилал"

    def __unicode__(self):
        return self.name

class Partner(models.Model):
    name = models.CharField(u'Нэр', max_length=128)
    description = models.TextField(u'Тайлбар', blank=True, required=False)
    category_id = models.ForeignKey('PartnerCategory', verbose_name=u'Ангилал',
                related_name='partner_set')
    started_date = models.Date(u'Байгуулагдсан он', blank=True, required=False),
    user_id = models.ForeignKey('User', verbose_name=u'Хандах эрх', required=True)
    
    class Meta:
        verbose_name_plural = u"Харилцагчид"
        verbose_name = u"Харилцагч"

    def __unicode__(self):
        return self.name

class JobCategory(models.Model):
    name = models.CharField(u'Нэр', max_length=128),
    description = models.TextField(u'Тайлбар', blank=True, required=False)
    
    class Meta:
        verbose_name_plural = u"Ажлын ангилалууд"
        verbose_name = u"Ажлын ангилал"

    def __unicode__(self):
        return self.name

class JobLevel(models.Model):
    name = models.CharField(u'Нэр', max_length=128),
    description = models.TextField(u'Тайлбар', blank=True, required=False)
    
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
    deadline = models.Date(u'Эцсийн огноо', help_text=u'Хэрэв эцсийн огноо оруулахгүй бол уг ажлын байр байнга нээлттэй байх болно.'),
    
