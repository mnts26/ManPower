#!coding=utf8
from django.db import models
from django.contrib.auth.models import User 
from common.models import *
import time

# Create your models here.
class PartnerCategory(models.Model):
    name = models.CharField(u'Нэр', max_length=64)
    parent = models.ForeignKey('self', verbose_name=u'Эцэг ангилал', 
                related_name='child_set', blank=True, null=True)
    description = models.TextField(u'Тайлбар', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = u"Харилцагчийн ангилалууд"
        verbose_name = u"Харилцагчийн ангилал"

    def __unicode__(self):
        return self.name

class Partner(models.Model):
    name = models.CharField(u'Нэр', max_length=128)
    description = models.TextField(u'Тайлбар', blank=True, null=True)
    logo = models.ImageField(upload_to='partners/%Y/%m/%d', null=True, blank=True)
    poster = models.CharField(u'Уриа' , max_length=256 ,null=True, blank=True)
    website = models.CharField(u'Вэб хуудас' , max_length=256 ,null=True, blank=True)
    category_id = models.ForeignKey('PartnerCategory', verbose_name=u'Ангилал',related_name='partner_set')
    started_date = models.DateField(u'Байгуулагдсан он', blank=True, null=True)
    user = models.ForeignKey(User, verbose_name=u'Хандах эрх', blank=True, null=True)
    level = models.CharField(u'Зэрэглэл', choices=[('gold',u'Алт'),('silver',u'Мөнгө'),('bronze',u'Хүрэл'),('other',u'Бусад')], max_length=10)
    class Meta:
        verbose_name_plural = u"Харилцагчид"
        verbose_name = u"Харилцагч"

    def admin_image(self):
        if self.logo:
            return u'<img src="%s" />' % self.logo
        else:
            return u'(Зураггүй)'
        admin_image.short_description = 'Thumb'
        admin_image.allow_tags = True


    def __unicode__(self):
        return self.name

class JobCategory(models.Model):
    name = models.CharField(u'Нэр', max_length=128)
    parent = models.ForeignKey('self', verbose_name=u'Эцэг ангилал', 
                related_name='child_set', blank=True, null=True)
    description = models.TextField(u'Тайлбар', blank=True, null=True)
    
    def menu_html(self, parent=True ):
        count_job = JobOrder.objects.filter(category = self.pk ) 
        a = count_job.count()
        html = u''
        if parent:
            html += u'<a href="/base/joblist/%s" class="parent">%s  (%d) </a>\n' % (self.id, self.name  , a)
            html += u'<span class="closedmenu"></span>\n'
            html += u'<div style="display: block">\n'
            html += u'<ul>\n'
        else :
            html += u'<li>\n'
            html += u'<span class="closedmenu"></span>\n'
            html += u'<a href="/base/joblist/%s">%s</a>\n' % (self.id, self.name)
            html += u'<div style="display: block">\n'
            html += u'<ul>\n'
        for child in self.child_set.all() :
            html += child.menu_html(parent=False)
        html += u'</ul>\n'
        html += u'</div>'
        return html
    
    def path(self):
        
        html = '<span>/</span><a href="/base/joblist/%s"><strong>%s</strong></a>' % (self.id, self.name)
        if self.parent:
            html = self.parent.path() + html
        return html
    
    def get_all_children(self):
        r = []
        r.append(self)
        for c in JobCategory.objects.filter(parent=self):
           r.extend(c.get_all_children())
        return r
    
    class Meta:
        verbose_name_plural = u"Ажлын ангилалууд"
        verbose_name = u"Ажлын ангилал"

    def __unicode__(self):
        return self.name

class JobLevel(models.Model):
    name = models.CharField(u'Нэр', max_length=128)
    description = models.TextField(u'Тайлбар', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = u"Ажлын зэрэглэлүүд"
        verbose_name = u"Ажлын зэрэглэл"

    def __unicode__(self):
        return self.name

class JobOrder(models.Model):
    category = models.ForeignKey('JobCategory', verbose_name=u'Ангилал', related_name='joborder_set')
    partner = models.ForeignKey('Partner', verbose_name=u'Байгууллага', related_name='joborder_set')
    level = models.ForeignKey('JobLevel', verbose_name=u'Зэрэглэл', related_name='joborder_set')
    name = models.CharField(u'Нэр', max_length=128)
    funtional = models.TextField(u'Гүйцэтгэх үндсэн үүрэг')
    description = models.TextField(u'Тайлбар', blank=True, null=True)
    requirement = models.TextField(u'Тавигдах шаардлага')
    salary = models.CharField(u'Цалин', null=True, blank=True, default=u'Тохиролцоно', max_length=64)
    deadline = models.DateField(u'Эцсийн огноо', help_text=u'Хэрэв эцсийн огноо оруулахгүй бол уг ажлын байр байнга нээлттэй байх болно.', null=True, blank=True)
    active = models.BooleanField(u'Идэвхитэй', help_text=u'Уг ажлын байр ажил горилогчид харагдах эсэх',default=True)
    create_date = models.DateField(u'Үүсгэсэн огноо', auto_now_add=True)
    class Meta:
        verbose_name_plural = u"Ажлын байрууд"
        verbose_name = u"Ажлын байр"

    def __unicode__(self):
        return self.name

class JobCv(models.Model):
    order = models.ForeignKey('JobOrder', verbose_name=u'Ажлын захиалга', related_name='jobapplication_set')
    email = models.EmailField(u'Е-майл хаяг', max_length=128, blank=True, null=True)
    last_name = models.CharField(u'Эцгийн нэр', max_length=64)
    first_name = models.CharField(u'Өөрийн нэр', max_length=64)
    family_name = models.CharField(u'Ургийн овог', max_length=64, blank=True, null=True)
    gender = models.CharField(u'Хүйс', choices=[('male',u'Эрэгтэй'),('female',u'Эмэгтэй')], max_length=10, default='male')
    birthdate = models.DateField(u'Төрсөн он сар өдөр')
    nation = models.CharField(u'Үндэс угсаа', max_length=64, blank=True, null=True)
    home_address = models.CharField(u'Гэрийн хаяг', max_length=512)
    birthcity = models.ForeignKey(CommonCity, verbose_name=u'Төрсөн аймаг, хот', blank=True, null=True)
    birthdistrict = models.ForeignKey(CommonDistrict, verbose_name=u'Төрсөн сум, дүүрэг', related_name='birthdistrict_set', blank=True, null=True)
    education = models.ForeignKey(CommonEducation, verbose_name=u'Боловсрол')
    occupation = models.CharField(u'Мэргэжил', max_length=64, blank=True, null=True)
    passnumber = models.CharField(u'Иргэний үнэмлэхний дугаар', max_length=64, null=True, blank=True)
    registernumber = models.CharField(u'Регистерийн дугаар', max_length=64)
    socialstatus = models.ForeignKey(CommonSocialStatus, verbose_name=u'Нийгмийн гарал', null=True, blank=True)
    district = models.ForeignKey(CommonDistrict, verbose_name=u'Үндсэн захиргаа', related_name='district_set', null=True, blank=True)
    
    method_return = models.CharField(u'Холбоо барих хэлбэр', help_text=u'Тантай эргэн холбоо барих хэлбэр',
                                     choices=[('phone', u'Утсаар'),('email', u'E-mail')], max_length=10, default='phone')
    salary_request = models.DecimalField(u'Цалингийн хүлээлт', help_text=u'Хүсэж буй цалингийн доод хэмжээг бичнэ үү',
                                         max_digits=16, decimal_places=2, null=True, blank=True)
    date_posible = models.DateField(u'Боломжит хугацаа', help_text=u'Таны ШИНЭ компанид ажилд орох боломжтой хугацаа',
                                    null=True, blank=True)
    date_created = models.DateField(u'Бүртгэсэн огноо')
    photo = models.ImageField(upload_to='uploads/CVphoto/')
    
    class Meta:
        verbose_name_plural = u"Ажил горилогчийн анкетууд"
        verbose_name = u"Ажил горилогчийн анкет"

    def __unicode__(self):
        return self.name

class JobCvPhone(models.Model):
    type = models.CharField(u'Төрөл', choices=[
            ('home',u'Гэр'),
            ('mobile',u'Гар'),
            ('work',u'Ажил'),
            ('other',u'Бусад')], max_length=10, default='home')
    number = models.CharField(u'Дугаар', max_length=32)
    cv = models.ForeignKey('JobCv', verbose_name=u'Анкет', related_name='phone_set')
    
    class Meta:
        verbose_name_plural = u"Утасны дугаарууд"
        verbose_name = u"Утасны дугаар"

    def __unicode__(self):
        return u'%s %s' % (self.type, self.number)

class JobCvEducation(models.Model):
    TYPE_CHOICES = [
        ('a', u'Бакалавар'),
        ('b', u'Магистр'),
        ('c', u'Доктор'),
        ('d', u'Бүрэн дунд'),
        ('e', u'Тусгай дунд'),
        ('f', u'Дээд')
    ]
    type = models.CharField(u'Төрөл', choices=TYPE_CHOICES, max_length=10)
    name = models.CharField(u'Сургуулийн нэр', max_length=64)
    start_year = models.CharField(u'Элссэн он', max_length=5)
    end_year = models.CharField(u'Төгссөн/төгсөх он', max_length=5)
    occupation = models.CharField(u'Эзэмшсэн мэргэжил', max_length=64, null=True, blank=True)
    country = models.ForeignKey(CommonCountry, verbose_name=u'Улс', null=True, blank=True)
    meridian = models.DecimalField(u'Голч дүн', max_digits=3, decimal_places=2, null=True, blank=True)
    cv = models.ForeignKey('JobCv', verbose_name=u'Анкет', related_name='education_set')
    
    class Meta:
        verbose_name_plural = u"Боловсролын бүртгэлүүд"
        verbose_name = u"Боловсролын бүртгэл"

    def __unicode__(self):
        return u'%s %s' % (self.type, self.name)

class JobCvCourse(models.Model):
    name = models.CharField(u'Нэр', max_length=64)
    start_year = models.CharField(u'Элссэн он', max_length=5)
    end_year = models.CharField(u'Төгссөн/төгсөх он', max_length=5)
    occupation = models.CharField(u'Эзэмшсэн мэргэжил', max_length=64, null=True, blank=True)
    certificate = models.CharField(u'Сертификат, үнэмлэхний дугаар', max_length=64, null=True, blank=True)
    cv = models.ForeignKey('JobCv', verbose_name=u'Анкет', related_name='course_set')
    
    class Meta:
        verbose_name_plural = u"Курс дамжаа бүртгэлүүд"
        verbose_name = u"Дурс дамжаа бүртгэл"

    def __unicode__(self):
        return u'%s %s' % (self.type, self.name)

class JobCvForeignLanguage(models.Model):
    LANG_LEVEL_CHOICES = [
        ('high', u'Сайн'),
        ('medium', u'Дунд'),
        ('low', u'Анхан шат')
    ]
    language = models.ForeignKey(CommonLanguage, verbose_name=u'Хэл')
    period = models.IntegerField('Үзсэн хугацаа(сар)', null=True, blank=True)
    understand = models.CharField(u'Ярьсныг ойлгох', max_length=10, choices=LANG_LEVEL_CHOICES, default='medium')
    speak = models.CharField(u'Өөрөө ярих', max_length=10, choices=LANG_LEVEL_CHOICES, default='medium')
    read = models.CharField(u'Уншиж ойлгох', max_length=10, choices=LANG_LEVEL_CHOICES, default='medium')
    write = models.CharField(u'Бичиж орчуулах', max_length=10, choices=LANG_LEVEL_CHOICES, default='medium')
    cv = models.ForeignKey('JobCv', verbose_name=u'Анкет', related_name='language_set')
    
    class Meta:
        verbose_name_plural = u"Гадаад хэлний мэдлэгүүд"
        verbose_name = u"Гадаад хэлний мэдлэг"

    def __unicode__(self):
        return self.language

class JobCvSkill(models.Model):
    SKILL_LEVEL_CHOICES = [
        ('high', u'Бүрэн эзэмшсэн'),
        ('medium', u'Хэрэглээний түвшинд'),
        ('low', u'Анхан шатны')
    ]
    name = models.CharField(u'Программ', max_length=128)
    level = models.CharField(u'Түвшин', choices=SKILL_LEVEL_CHOICES, max_length=10)
    cv = models.ForeignKey('JobCv', verbose_name=u'Анкет', related_name='skill_set', null=True, blank=True)
    
    class Meta:
        verbose_name_plural = u"Компьютерын мэдлэгүүд"
        verbose_name = u"Компьютерын мэдлэг"

    def __unicode__(self):
        return u'%s - %s' %(self.name, dict(SKILL_LEVEL_CHOICES).get(self.level, ''))

class JobCvUsage(models.Model):
    USAGE_LEVEL_CHOICES = [
        ('high', u'Онц'),
        ('medium', u'Сайн'),
        ('low', u'Дунд')
    ]
    name = models.CharField(u'Тоног төхөөрөмж', max_length=128)
    level = models.CharField(u'Түвшин', choices=USAGE_LEVEL_CHOICES, max_length=10)
    cv = models.ForeignKey('JobCv', verbose_name=u'Анкет', related_name='usage_set', null=True, blank=True)
    
    class Meta:
        verbose_name_plural = u"Оффисын мэдлэгүүд"
        verbose_name = u"Оффисын мэдлэг"

    def __unicode__(self):
        return u'%s - %s' %(self.name, dict(USAGE_LEVEL_CHOICES).get(self.level, ''))

class JobCvWorking(models.Model):
    name = models.CharField(u'Байгууллагын нэр', max_length=128)
    address = models.CharField(u'Хаяг', max_length=512, null=True, blank=True)
    category = models.ForeignKey('PartnerCategory', verbose_name=u'Салбар')
    date_start = models.DateField(u'Ажилд орсон огноо', null=True, blank=True)
    date_stop = models.DateField(u'Ажлаас гарсан огноо', null=True, blank=True)
    position = models.CharField(u'Албан тушаал', max_length=128, null=True, blank=True)
    reason = models.CharField(u'Ажлаас гарсан шалтгаан', max_length=512, null=True, blank=True)
    cv = models.ForeignKey('JobCv', verbose_name=u'Анкет', related_name='working_set', null=True, blank=True)
    
    class Meta:
        verbose_name_plural = u"Ажил эрхлэлтийн бүртгэлүүд"
        verbose_name = u"Ажил эрхлэлтийн бүртгэл"

    def __unicode__(self):
        return u'%s - %s (%s)' %(self.name, (self.position or ''), self.category.name)

class JobCvRelation(models.Model):
    RELATION_REFERENCE_TYPE = [
        ('father', u'Аав'),
        ('mother', u'Ээж'),
        ('gfather', u'Өвөө'),
        ('gmother', u'Эмээ'),
        ('brother', u'Ах'),
        ('sister', u'Эгч'),
        ('ybrother', u'Дүү'),
        ('wife', u'Эхнэр'),
        ('husband', u'Нөхөр'),
        ('son', u'Хүү'),
        ('daughter', u'Охин')
    ]
    
    reference = models.CharField(u'Хамаарал', choices=RELATION_REFERENCE_TYPE, max_length=10)
    last_name = models.CharField(u'Эцгийн нэр', max_length=64, null=True, blank=True)
    first_name = models.CharField(u'Өөрийн нэр', max_length=64)
    working = models.CharField(u'Байгууллагын нэр', max_length=64, null=True, blank=True)
    position = models.CharField(u'Албан тушаал', max_length=64, null=True, blank=True)
    phone = models.CharField(u'Холбогдох утас', max_length=20, null=True, blank=True)
    email = models.CharField(u'И-мэйл', max_length=64, null=True, blank=True)
    cv = models.ForeignKey('JobCv', verbose_name=u'Анкет', related_name='relation_set', null=True, blank=True)
    
    class Meta:
        verbose_name_plural = u"Гэр бүлийн бүртгэлүүд"
        verbose_name = u"Гэр бүлийн бүртгэл"

    def __unicode__(self):
        return u'%s - %s %s' %(dict(RELATION_REFERENCE_TYPE).get(self.reference,''), (self.last_name or ''), self.first_name)

