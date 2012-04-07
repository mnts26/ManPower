#coding:utf-8
"""
@copyright: Jacara
@contact: baskhuujacara@gmail.com; baskhuu@usi.mn
@summary: forms of Android Site Base module
"""
from django import forms
from django.forms import ModelForm
from usiextensions import forms as extForms
from base.models import *
import datetime
#from captcha.fields import CaptchaField, JavaChallengeField
#from django.utils.translation import ugettext_lazy as _
import re

class JobCvForm(extForms.extModelForm) :
    birthcity = extForms.extModelChoiceField(label=u'Төрсөн аймаг, хот', model=CommonCity, 
                search='name', display=('name',))
    birthdistrict = extForms.extModelChoiceField(label=u'Төрсөн сум, дүүрэг', model=CommonDistrict, 
                search='name', display=('name','city__name'))
    education = extForms.extModelChoiceField(label=u'Боловсрол', model=CommonEducation, 
                search='name', display=('name',))
    socialstatus = extForms.extModelChoiceField(label=u'Нийгмийн гарал', model=CommonSocialStatus, 
                search='name', display=('name',))
    district = extForms.extModelChoiceField(label=u'Үндсэн захиргаа', model=CommonDistrict, 
                search='name', display=('name','city__name'))
    salary_request = extForms.extDecimalField(label=u'Цалингийн хүлээлт', widget=extForms.extDecimalWidget)
    home_address = extForms.extCharField(label=u'Гэрийн хаяг', widget=extForms.extTextarea({'rows':5}))
    gender = forms.CharField(label=u'Хүйс', max_length=10, widget=extForms.extSelect({'width':'120'},
            choices=[('male',u'Эрэгтэй'),('female',u'Эмэгтэй')]), initial='male')
    
    class Meta:
        model = JobCv
        exclude = ['order','date_created']
#        sequence = [
#            (_('Basic Information'), ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']),
#            (_('Profile Information'), ['website','location','occupation','interest','signature']),
#            (_('Preferences'), ['show_email','hide_online','notify_reply','attach_signature', 'board_language'])
#        ]
    
#class MemberProfileForm(extForms.extModelForm):
#    last_name       = forms.CharField(label=_("Last name"), required=True)
#    first_name      = forms.CharField(label=_("First name"), required=True)
#    email           = forms.EmailField(label=_("E-Mail address"), required=True)
#    location        = extForms.extModelChoiceField(label=_("Location"), model=Location, 
#                search='name', display=('name','code'), required=True)
#    
#    def clean_username(self) :
#        username = self.cleaned_data["username"]
#        try :
#            User.objects.exclude(pk=self.instance.pk).get(username=username)
#        except User.DoesNotExist :
#            return username
#        raise forms.ValidationError(_("A user with that username already exists."))
#
#    def save(self, commit=True) :
#        user = super(MemberProfileForm, self).save(commit=False)
#        if commit:
#            user.save()
#        return user
#    
#    class Meta :
#        model = Member
#        exclude = ['password', 'is_active', 'is_superuser', 'last_login',
#                    'date_joined', 'groups', 'user_permissions', 'is_staff', 'board_style']
#        sequence = [
#            (_('Basic Information'),['username', 'first_name', 'last_name', 'email']),
#            (_('Profile Information'),['location', 'website','occupation','interest','signature']),
#            (_('Preferences'),['show_email','hide_online','notify_reply','attach_signature',
#                               'board_language'])
#        ]
#
#class NewsCommentForm(extForms.extModelForm) :
#    captcha         = CaptchaField(label=_('Are you a human?'), required=True)
#    comment         = extForms.extCharField(widget=extForms.extRichTextEditor(), required=True)
#    
#    class Meta :
#        model = NewsComment
#        exclude = ["news", "date"]
#        sequence = [
#            (_('Add comment'), ['commented_by','email','comment','captcha']),
#        ]
#
#class ToturialCommentForm(extForms.extModelForm) :
#    captcha         = CaptchaField(label=_('Are you a human?'), required=True)
#    comment         = extForms.extCharField(widget=extForms.extRichTextEditor(), required=True)
#    
#    class Meta :
#        model = ToturialComment
#        exclude = ["toturial", "date"]
#        sequence = [
#            (_('Add comment'), ['commented_by','email','comment','captcha']),
#        ]

class JobOrderForm(extForms.extModelForm) :
    category = extForms.extModelChoiceField(label=u'Ангилал', model=JobCategory, search='name', display=('parent__name','name',))
    level =  extForms.extModelChoiceField(label=u'Зэрэглэл', model=JobLevel, search='name', display=('name',))
    partner = forms.CharField(widget=forms.HiddenInput(), label='Байгууллага')
    
    def clean_partner(self):
        data = self.cleaned_data
        try:
            Partner.objects.get(username = data['partner'])
        except User.DoesNotExist:
            return data['partner']
        raise forms.ValidationError('This partner is already taken.')
    def save(self, user, *args, **kwargs):
        self.instance.partner = user
        self.instance.create_date = datetime.date.today()
        post = super(JobOrderForm, self).save(*args, **kwargs)
        post.save()
        return post

    class Meta:
        model = JobOrder
        exclude = ['create_date']

class JobCvPhoneForm(extForms.extModelForm):
    type = forms.CharField(label=u'Төрөл', max_length=10, widget=extForms.extSelect({'width':'150'}, choices=[
            ('', u'-----'),
            ('home',u'Гэр'),
            ('mobile',u'Гар'),
            ('work',u'Ажил'),
            ('other',u'Бусад')]))
    number = extForms.extCharField(label=u'Дугаар', max_length=32, widget=extForms.extIntegerWidget())
    
    class Meta:
        model = JobCvPhone
        
class JobCvEducationForm(extForms.extModelForm):
    def _get_year_choices():
        years = []
        this_year = int(time.strftime('%Y'))
        for x in range(this_year-80, this_year) :
            years.append( (x, str(x)) )
        return years
    
    YEAR_CHOICES = _get_year_choices()
    type = forms.CharField(label=u'Төрөл', max_length=10, widget=extForms.extSelect({'width':'100'}, choices=[
        ('',  u'-----'),
        ('a', u'Бакалавар'),
        ('b', u'Магистр'),
        ('c', u'Доктор'),
        ('d', u'Бүрэн дунд'),
        ('e', u'Тусгай дунд'),
        ('f', u'Дээд')]))
    start_year = extForms.extCharField(label=u'Элссэн он', max_length=4, widget=extForms.extSelect({'width':'80'},choices=YEAR_CHOICES))
    end_year = extForms.extCharField(label=u'Төгссөн/төгсөх он', max_length=4, widget=extForms.extSelect({'width':'80'},choices=YEAR_CHOICES))
    country = extForms.extModelChoiceField(label=u'Улс', model=CommonCountry, required=False,
                    search='name', display=('name',), cwidth=130)
    name = extForms.extCharField(label=u'Сургууль', max_length=64, widget=extForms.extTextInput({'style':'width:200px'}))
    occupation = extForms.extCharField(label=u'Мэргэжил', max_length=64, widget=extForms.extTextInput({'style':'width:200px'}))
    meridian = extForms.extDecimalField(label=u'Голч дүн', max_digits=3, decimal_places=2, required=False)
    
    class Meta:
        model = JobCvEducation

class JobCvCourseForm(extForms.extModelForm):
    def _get_year_choices():
        years = []
        this_year = int(time.strftime('%Y'))
        for x in range(this_year-80, this_year) :
            years.append( (x, str(x)) )
        return years
    
    YEAR_CHOICES = _get_year_choices()
    name = extForms.extCharField(label=u'Курс', max_length=64, widget=extForms.extTextInput({'style':'width:200px'}))
    start_year = extForms.extCharField(label=u'Элссэн он', max_length=4, widget=extForms.extSelect({'width':'80'},choices=YEAR_CHOICES))
    end_year = extForms.extCharField(label=u'Төгссөн/төгсөх он', max_length=4, widget=extForms.extSelect({'width':'80'},choices=YEAR_CHOICES))
    occupation = extForms.extCharField(label=u'Мэргэжил', max_length=64, widget=extForms.extTextInput({'style':'width:200px'}))
    
    class Meta:
        model = JobCvCourse

class JobCvLanguageForm(extForms.extModelForm):
    LANG_LEVEL_CHOICES = [
        ('high', u'Сайн'),
        ('medium', u'Дунд'),
        ('low', u'Анхан шат')
    ]
    period = extForms.extIntegerField(label=u'Үзсэн хугацаа', required=False)
    language = extForms.extModelChoiceField(label=u'Хэл', model=CommonLanguage, 
                    search='name', display=('name',), cwidth=130)
    understand = extForms.extCharField(label=u'Ярьсныг ойлгох', max_length=10, widget=extForms.extSelect({'width':120},choices=LANG_LEVEL_CHOICES), initial='medium')
    speak = extForms.extCharField(label=u'Өөрөө ярих', max_length=10, widget=extForms.extSelect({'width':120},choices=LANG_LEVEL_CHOICES), initial='medium')
    read = extForms.extCharField(label=u'Уншиж ойлгох', max_length=10, widget=extForms.extSelect({'width':120},choices=LANG_LEVEL_CHOICES), initial='medium')
    write = extForms.extCharField(label=u'Бичиж орчуулах', max_length=10, widget=extForms.extSelect({'width':120},choices=LANG_LEVEL_CHOICES), initial='medium')
    
    class Meta:
        model = JobCvForeignLanguage

class JobCvSkillForm(extForms.extModelForm):
    SKILL_LEVEL_CHOICES = [
        ('high', u'Бүрэн эзэмшсэн'),
        ('medium', u'Хэрэглээний түвшинд'),
        ('low', u'Анхан шатны')
    ]
    name = extForms.extCharField(label=u'Программын нэр', max_length=128, widget=extForms.extTextInput({'style':'width:200px'}))
    level = extForms.extCharField(label=u'Түвшин', max_length=10, widget=extForms.extSelect({'width':120},choices=SKILL_LEVEL_CHOICES))
    class Meta:
        model = JobCvSkill
    
class JobCvUsageForm(extForms.extModelForm):
    USAGE_LEVEL_CHOICES = [
        ('high', u'Онц'),
        ('medium', u'Сайн'),
        ('low', u'Дунд')
    ]
    name = extForms.extCharField(label=u'Тоног төхөөрөмжийн нэр', max_length=128, widget=extForms.extTextInput({'style':'width:200px'}))
    level = extForms.extCharField(label=u'Түвшин', max_length=10, widget=extForms.extSelect({'width':120},choices=USAGE_LEVEL_CHOICES))
    class Meta:
        model = JobCvUsage

class JobCvWorkingForm(extForms.extModelForm):
    name = extForms.extCharField(label=u'Байгууллагын нэр', max_length=128, widget=extForms.extTextInput({'style':'width:160px'}))
    address = extForms.extCharField(label=u'Хаяг', max_length=512, widget=extForms.extTextInput({'style':'width:200px'}))
    category = extForms.extModelChoiceField(label=u'Хэл', model=PartnerCategory,
                    search='name', display=('name',), cwidth=160)
    position = extForms.extCharField(label=u'Албан тушаал', max_length=128, widget=extForms.extTextInput({'style':'width:170px'}))
    class Meta:
        model = JobCvWorking
        
class JobCvRelationForm(extForms.extModelForm):
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
    reference = extForms.extCharField(label=u'Хамаарал', max_length=10, widget=extForms.extSelect({'width':120},choices=RELATION_REFERENCE_TYPE))
    working = extForms.extCharField(label=u'Байгууллагын нэр', max_length=64, widget=extForms.extTextInput({'style':'width:190px'}), required=False)
    position = extForms.extCharField(label=u'Албан тушаал', max_length=64, widget=extForms.extTextInput({'style':'width:190px'}), required=False)
    phone = extForms.extCharField(label=u'Утас', max_length=20, widget=extForms.extIntegerWidget({'style':'width:120px'}))
    
    class Meta:
        model = JobCvRelation

from django.forms.models import BaseInlineFormSet

class PhoneInlineFormSet(BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count < 1:
            raise forms.ValidationError(u'Та дор хаяж нэг утасны дугаар бүртгэх шаардлагатай !')