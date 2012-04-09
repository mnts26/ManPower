#coding:utf-8
from django.contrib import admin
from base.models import *
from usiextensions.widgets import extRichTextEditor2, extModelSelect
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe

class AdminImageWidget(AdminFileWidget) :
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = '/media/uploaded/' + value.url
            file_name=str(value)
            output.append(u' <a href="%s" target="_blank"><img src="%s" alt="%s" /></a><br/> %s ' % \
                (image_url, image_url, file_name, _('Солих:')))
        output.append(super(AdminImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
    


class PartnerCategoryAdmin(admin.ModelAdmin):
    fieldsets = ((u'Ерөнхий', {'fields':('name','parent','description')}),)
    list_display = ('parent','name','description')
    search_fields = ('name','parent')
admin.site.register(PartnerCategory, PartnerCategoryAdmin)

class PartnerAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'logo':
            kwargs['widget'] = AdminImageWidget
            try:
                del kwargs['request']
            except KeyError:
                pass
            return db_field.formfield(**kwargs)
        return super(PartnerAdmin,self).formfield_for_dbfield(db_field, **kwargs)
    
    formfield_overrides = {
        models.TextField: {'widget': extRichTextEditor2},
    }
    fieldsets = ((u'Ерөнхий', {'fields':('name','category_id','poster','logo','website')}),
                 (u'Нэмэлт', {'fields':('description','started_date','level')}),
                 (u'Портал хандалт', {'fields':('user',)}))
    list_display = ('level','admin_image','name','category_id','user')
    search_fields = ('name','category_id','user')
    list_filter = ('level',)
admin.site.register(Partner, PartnerAdmin)

class JobCategoryAdmin(admin.ModelAdmin):
    fieldsets = ((u'Ерөнхий', {'fields':('name','parent')}),
                 (u'Тайлбар', {'fields':('description',)}))
    list_display = ('name','parent','description')
    search_fields = ('name','parent')
admin.site.register(JobCategory, JobCategoryAdmin)

class JobOrderAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': extRichTextEditor2},
        #models.ForeignKey: {'widget': extModelSelect}
    }
    
    fieldsets = ((u'Ерөнхий мэдээлэл', {'fields':('category','partner','level','name','functional')}),
                 (u'Бусад мэдээлэл', {'fields':('description','requirement','salary','deadline','active')}))
    list_display = ('category','name','partner','level','deadline','active')
    search_fields = ('name','category','partner')
admin.site.register(JobOrder, JobOrderAdmin)

class JobLevelAdmin(admin.ModelAdmin):
    fieldsets = ((u'Ерөнхий', {'fields':('name',)}),
                 (u'Тайлбар', {'fields':('description',)}))
    list_display = ('name','description')
    search_fields = ('name',)
admin.site.register(JobLevel, JobLevelAdmin)




