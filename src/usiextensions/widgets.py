#coding:utf-8
"""
@author: Jacara
@summary: USI Extensions Custom Widgets 
"""

from django import forms
from django.db import models
# for Custom Widget
from django.forms.util import flatatt
from django.utils.encoding import smart_unicode
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape
from django.utils.translation import ugettext
from itertools import chain

# Calendar widget
# Монгол хэрэглээнд тохируулж өргөтгөсөн.
class extDateWidget(forms.TextInput) :
    class Media:
        css = {
            'all': ('/extmedia/css/jquery.datepicker.css',
                    '/extmedia/css/widgets.css',)
        }
        js = (
              #'/extmedia/script/jquery-1.3.2.min.js',
              '/extmedia/script/jquery.datepicker.js',
        )
        
    def render(self, name, value, attrs=None) :
        input = u'<input type="text" value="%s" name="%s" id="id_%s" class="extTextInput"/>' % (value or '', name, name)
        script = u'''<script type="text/javascript">
            jQuery('#id_%s')
                .datepicker({ 
                    dateFormat: 'yy-mm-dd',
                    dayNames: ['Даваа', 'Мягмар', 'Лхагва', 'Пүрэв', 'Баасан', 'Бямба', 'Ням'],
                    dayNamesMin: ['Да', 'Мя', 'Лх', 'Пү', 'Ба', 'Бя', 'Ня'],
                    dayNamesShort: ['Дав', 'Мяг', 'Лха', 'Пүр', 'Баа', 'Бям', 'Ням'],
                    duration: 'slow',
                    firstDay: 1
                })
                .css({'color':'#666666','text-align':'center','width':'85px'});
        </script>''' % name
        return mark_safe(input + script)

class extTimeWidget(forms.TextInput):
    ''' Usage :
            <div id="timepicker">
    '''
    class Media:
        css = {
            'all': ('/extmedia/css/jquery.timeentry.css','/extmedia/css/widgets.css')
        }
        js = (
              #'/extmedia/script/jquery-1.3.2.min.js',
              '/extmedia/script/jquery.timeentry.min.js'
        )
    
    def render(self, name, value, attrs=None) :
        input = u'<input type="text" value="%s" name="%s" id="id_%s" class="extTextInput">' % (value or '', name, name)
#        input += u'<img src="data/clock.png" alt="Time" border="0" style="position:absolute;margin:4px 0 0 6px;" id="trigger-test" />'
        script = u'''<script type="text/javascript">
            jQuery('#id_%s')
                .timeEntry({
                    spinnerImage  : '/extmedia/images/spinnerOrange.png',
                    spinnerBigImage : '/extmedia/images/spinnerOrangeBig.png',
                    spinnerSize   : [20, 20, 0],
                    spinnerBigSize: [40, 40, 0]
                })
                .css({'color':'#666666','text-align':'center','width':'100px'});
        </script>''' % name
        return mark_safe(input + script)


class extTextInput(forms.TextInput):
    class Media:
        css = {
            'all': ('/extmedia/css/widgets.css',)
        }
    
    def render(self, name, value, attrs=None) :
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        final_attrs.update({'class':'extTextInput'})
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(value)
        return mark_safe(u'<input%s />' % flatatt(final_attrs))

class extPasswordInput(forms.PasswordInput):
    class Media:
        css = {
            'all': ('/extmedia/css/widgets.css',)
        }
    
    input_type = 'password'
    
    def __init__(self, attrs=None, render_value=True):
        super(extPasswordInput, self).__init__(attrs, render_value=True)
    
    def render(self, name, value, attrs=None) : 
        if not self.render_value or not value :
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        final_attrs.update({'class':'extTextInput'})
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(value)
        return mark_safe(u'<input%s />' % flatatt(final_attrs))

class extTextarea(forms.Textarea):
    class Media:
        css = {
            'all': ('/extmedia/css/widgets.css',)
        }
    
    def __init__(self, attrs=None):
        # The 'rows' and 'cols' attributes are required for HTML correctness.
        self.attrs = {'cols': '40', 'rows': '10'}
        if attrs:
            self.attrs.update(attrs)

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        value = force_unicode(value)
        final_attrs = self.build_attrs(attrs, name=name)
        final_attrs.update({'class':'extTextArea'})
        return mark_safe(u'<textarea%s>%s</textarea>' % (flatatt(final_attrs),
                conditional_escape(force_unicode(value))))

class extRichTextEditor(forms.Textarea) :
    class Media :
        css = {
            'all': ('/extmedia/css/jquery.markitup.min.css',
                    '/extmedia/css/jquery.markitup.sets.css')
        }
        js = (#'/extmedia/script/jquery-1.3.2.min.js',
              '/extmedia/script/jquery.markitup.js',
              '/extmedia/script/jquery.markitup.sets.js')
    
    def __init__(self, attrs=None) :
        self.attrs = {}
        if attrs :
            self.attrs.update(attrs)
        
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        value = force_unicode(value)
        final_attrs = self.build_attrs(attrs, name=name)
        script = u'''<script type="text/javascript">
            jQuery("#id_%s").markItUp(mySettings);
        </script>'''%name
        html = u'<table><tr><td><textarea%s>%s</textarea></td></tr></table>' % (flatatt(final_attrs), conditional_escape(force_unicode(value)))
        return mark_safe(html+script)

class extRichTextEditor2(forms.Textarea):
    class Media :
        css = {
            'all': ('/extmedia/css/jquery.markitup.css',
                    '/extmedia/css/jquery.markitup.sets.css')
        }
        js = ('/extmedia/script/jquery-1.3.2.min.js',
              '/extmedia/script/jquery.markitup.js',
              '/extmedia/script/jquery.markitup.sets.js')
    
    def __init__(self, attrs=None) :
        self.attrs = {}
        if attrs :
            self.attrs.update(attrs)
        
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        value = force_unicode(value)
        final_attrs = self.build_attrs(attrs, name=name)
        script = u'''<script type="text/javascript">
            jQuery("#id_%s").markItUp(mySettings);
        </script>'''%name
        html = u'<table><tr><td><textarea%s>%s</textarea></td></tr></table>' % (flatatt(final_attrs), conditional_escape(force_unicode(value)))
        return mark_safe(html+script)

        

class extIntegerWidget(extTextInput) :
    class Media:
        css = {
            'all': ('/extmedia/css/widgets.css',)
        }
        js = (#'/extmedia/script/jquery-1.3.2.min.js',
              '/extmedia/script/jquery.format.1.02.js',
              '/extmedia/script/jquery.example.min.js')
    
    def __init__(self, attrs=None):
        super(extIntegerWidget, self).__init__(attrs=attrs)
    
    def render(self, name, value, attrs=None) :
        if value is None:
            value = ''
        input = u'<input type="text" value="%s" name="%s" id="id_%s" class="extTextInput" %s/>' % (value, name, name, flatatt(self.attrs or {}))
        script = u'''<script type="text/javascript">
            jQuery("#id_%s")
                .format({precision: 0,autofix:true})
                .example(function() {return 'Тоо...!';},
                    {className: 'extNumberExampleLabel'});
        </script>''' % (name,)
        return mark_safe(input + script)

class extDecimalWidget(forms.TextInput) :
    class Media:
        css = {
            'all': ('/extmedia/css/widgets.css',)
        }
        js = (#'/extmedia/script/jquery-1.3.2.min.js',
              '/extmedia/script/jquery.format.1.02.js',
              '/extmedia/script/jquery.example.min.js')
        
    def render(self, name, value, attrs=None) :
        if not value:
            value = ''
        input = u'<input type="text" value="%s" name="%s" id="id_%s" class="extTextInput" %s/>' % (value, name, name, flatatt(self.attrs or {}))
        script = u'''<script type="text/javascript">
            jQuery("#id_%s")
                .format({precision: 2,autofix:true})
                .example(function() {return 'Тоон утга!';},
                    {className: 'extNumberExampleLabel'});
        </script>''' % name
        return mark_safe(input + script)

class extSelect(forms.Select):
    class Media:
        css = {
            'all': ('/extmedia/css/jquery.flexbox.css','/extmedia/css/widgets.css')
        }
        js = (
            #'/extmedia/script/jquery-1.3.2.min.js',
            '/extmedia/script/jquery.flexbox.min.js',
        )
    
    def __init__(self, attrs=None, choices=()):
        super(extSelect, self).__init__(attrs)
        # choices can be any iterable, but we may need to render this widget
        # multiple times. Thus, collapse it into a list so it can be consumed
        # more than once.
        self.choices = list(choices)
    
    def render(self, name, value, attrs=None, choices=()) :
        def _js_unicode(word):
            result = []
            for char in word:
                if ord(char) < 127:
                    result.append(char)
                else:
                    result.append(r'\u%04x' % ord(char))
            return ''.join(result)
        
        if self.choices :
            if value is None :
                value = u''
                
            total = 0
            results = "["
            add_hidden_value = ''
            for c in self.choices :
                c_name = str(_js_unicode(c[1]))
                if value == c[0] :
                    value = c_name
                    add_hidden_value = 'jQuery("#%s_hidden").val("%s");' % (name, c[0])
                results += '{"id":"%s","name":unescape("%s")},\n' % (c[0], c_name.replace("'",""))
                total += 1
            results = results[:-1]
            results += "]"
            input = u'<table><tr><td><div id="%s"></div></td></tr></table>' % name
            script = u"""
                <script type="text/javascript">
                    jQuery('#%(name)s').flexbox({"results": %(results)s, "total": %(total)s},
                        {
                        allowInput      : false,
                        initialValue    : unescape('%(value)s'),
                        width           : %(width)s,
                        resultTemplate  : '<table class="extFlexboxTable"><tr><td>{name}</td></tr></table>',
                        paging          : false,
                        maxVisibleRows  : 15
                        }
                    );
                    %(add_hidden_value)s
                </script>
            """ % ({'name':name,'results':results, 'total':total,'value':value,
                    'add_hidden_value':add_hidden_value,'width':self.attrs.get('width',230)})
            return mark_safe(input + script)
        else :
            search_name = self.attrs['search']
            model = self.attrs['model']
            if value is None or value == '' : 
                value = u''
                add_hidden_value = u''
                value_name = ''
            else :
                object = model.objects.get(pk=value)
                value_name = str(_js_unicode(getattr(object, search_name, u'')))
                add_hidden_value = 'jQuery("#%s_hidden").val("%s");' % (name, value)
            input = u'<table><tr><td><div id="%s"></div></td></tr></table>' % name
            template = u'<table class="extFlexboxTable"><tr>'
            display_names = []
            for d in self.attrs['display'] :
                template += u'<td class="row-left">{%s}</td>' % d
                display_names.append(d)
            display_names = ','.join(display_names)
            template += u'</tr></table>'
            script = u"""
                <script type="text/javascript">
                jQuery('#%(name)s').flexbox('/ext/forms/select/flexbox/%(object)s/%(search_name)s/%(display_names)s/', {
                    allowInput      : true,
                    displayValue    : '%(search_name)s',
                    hiddenValue     : 'id',
                    maxVisibleRows  : 0,
                    initialValue    : unescape('%(value_name)s'),
                    method          : 'POST',
                    watermark       : '%(watermark)s',
                    width           : %(width)s,
                    resultTemplate  : '%(template)s',
                    paging          : {
                        pageSize    : 15,
                        style       : 'input',
                        cssClass    : 'paging',
                        showSummary : true,
                        summaryTemplate : 'Нийт {total} өгөгдлөөс {start}-{end} ийг үзүүлж байна.'
                    },
                    onSelect: function() {
                        var value = this.getAttribute('hiddenValue');
                        if(value != '') {
                            jQuery('#%(name)s').val(value);
                        } else {
                            jQuery('#%(name)s_input').val('%(watermark)s').addClass('watermark');
                            jQuery('#%(name)s_hidden').val('');
                        }
                    },
                    noResultsListener : function() {
                        jQuery('#%(name)s_input').val('%(watermark)s').addClass('watermark');
                        jQuery('#%(name)s_hidden').val('');
                    },
                    noResultsText   : 'Тохирох утга олдсонгүй.'
                });
                %(add_hidden_value)s
                jQuery('#%(name)s_input').blur(function(e) {
                    if(jQuery.trim(jQuery(this).val()) == '') {
                        jQuery(this).val('%(watermark)s').addClass('watermark');
                        jQuery('#%(name)s_hidden').val('');
                    }
                });
                </script>
            """ % ({'name':name,'object':model._meta,'value_name':value,'template':template,'value_name':str(_js_unicode(value_name)),'width':self.attrs.get('width', 230),
                    'watermark':u'Бичнэ үү!','display_names':display_names,'search_name':search_name,'add_hidden_value':add_hidden_value})
            return mark_safe(input + script)

class extModelSelect(forms.Select):
    class Media:
        css = {
            'all': ('/extmedia/css/jquery.flexbox.css','/extmedia/css/widgets.css')
        }
        js = (
            #'/extmedia/script/jquery-1.3.2.min.js',
            '/extmedia/script/jquery.flexbox.min.js',
        )
    def __init__(self, attrs=None, choices=()):
        super(extModelSelect, self).__init__(attrs, choices=choices)
        model = self.attrs.get('model', None)
        if not model or not issubclass(model, models.Model) :
            raise Exception(u'extModelChoiceField-д model гэсэн models.Model-ын class дамжуулах ёстой.')
        if not self.attrs.get('search', None) :
            raise Exception(u'extModelChoiceField-д search гэсэн хайлт хийх талбарын нэрийг дамжуулах ёстой.')
        display = self.attrs.get('display', None)
        if not display or not isinstance(display, tuple) :
            raise Exception(u'extModelChoiceField-д display гэсэн tuple аргумент дамжуулах ёстой.')

    def render(self, name, value, attrs=None, choices=()) :
        search_name = self.attrs['search']
        model = self.attrs['model']
        if value is None or value == '' : 
            value = u''
            add_hidden_value = u''
            value_name = ''
        else :
            object = model.objects.get(pk=value)
            value_name = getattr(object, search_name, u'')
            add_hidden_value = 'jQuery("#%s_hidden").val("%s");' % (name, value)
        input = u'<table><tr><td><div id="%s"></div></td></tr></table>' % name
        template = u'<table class="extFlexboxTable"><tr>'
        display_names = []
        for d in self.attrs['display'] :
            template += u'<td class="row-left">{%s}</td>' % d
            display_names.append(d)
        display_names = ','.join(display_names)
        template += u'</tr></table>'
        script = u"""
            <script type="text/javascript">
            jQuery('#%(name)s').flexbox('/ext/forms/select/flexbox/%(object)s/%(search_name)s/%(display_names)s/', {
                allowInput      : true,
                displayValue    : '%(search_name)s',
                hiddenValue     : 'id',
                maxVisibleRows  : 0,
                initialValue    : '%(value_name)s',
                method          : 'POST',
                watermark       : '%(watermark)s',
                width           : %(width)s,
                resultTemplate  : '%(template)s',
                paging          : {
                    pageSize    : 15,
                    style       : 'input',
                    cssClass    : 'paging',
                    showSummary : true,
                    summaryTemplate : 'Нийт {total} өгөгдлөөс {start}-{end} ийг үзүүлж байна.'
                },
                onSelect: function() {
                    var value = this.getAttribute('hiddenValue');
                    if(value != '') {
                        jQuery('#%(name)s').val(value);
                    } else {
                        jQuery('#%(name)s_input').val('%(watermark)s').addClass('watermark');
                        jQuery('#%(name)s_hidden').val('');
                    }
                },
                noResultsListener : function() {
                    jQuery('#%(name)s_input').val('%(watermark)s').addClass('watermark');
                    jQuery('#%(name)s_hidden').val('');
                },
                noResultsText   : 'Тохирох утга олдсонгүй.'
            });
            %(add_hidden_value)s
            jQuery('#%(name)s_input').change(function(e) {
                if(jQuery.trim(jQuery(this).val()) == '') {
                    jQuery(this).val('%(watermark)s').addClass('watermark');
                    jQuery('#%(name)s_hidden').val('');
                }
            });
            </script>
        """ % ({'name':name,'object':model._meta,'value_name':value,'template':template,'value_name':value_name,'width':self.attrs.get('width',230),
                'watermark':u'Бичнэ үү!','display_names':display_names,'search_name':search_name,'add_hidden_value':add_hidden_value})
        return mark_safe(input + script)

class extNullBooleanSelect(forms.Select):
    """
    A Select Widget intended to be used with NullBooleanField.
    """
    class Media:
        css = {
            'all': ('/extmedia/css/widgets.css',)
        }
        js = (
              #'/extmedia/script/jquery-1.3.2.min.js',
              '/extmedia/script/custom.widgets.js',
        )
    def __init__(self, attrs=None):
        choices = ((u'1', ugettext('----------')), (u'2', ugettext('Yes')), (u'3', ugettext('No')))
        super(extNullBooleanSelect, self).__init__(attrs, choices)
    
    def render(self, name, value, attrs=None, choices=()):
        try:
            value = {True: u'2', False: u'3', u'2': u'2', u'3': u'3'}[value]
        except KeyError:
            value = u'1'
        if not attrs :
            attrs = {'class':'styled'}
        else :
            attrs.update({'class':'styled'})
        return super(extNullBooleanSelect, self).render(name, value, attrs=attrs, choices=choices)

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        return {u'2': True, u'3': False, True: True, False: False}.get(value, None)

    def _has_changed(self, initial, data):
        # Sometimes data or initial could be None or u'' which should be the
        # same thing as False.
        return bool(initial) != bool(data)

class extBooleanInput(forms.CheckboxInput):
    class Media:
        css = {
            'all': ('/extmedia/css/widgets.css',)
        }
        js = (
              #'/extmedia/script/jquery-1.3.2.min.js',
              '/extmedia/script/custom.widgets.js',
        )
    def __init__(self, attrs=None, check_test=bool):
        super(extBooleanInput, self).__init__(attrs)
        # check_test is a callable that takes a value and returns True
        # if the checkbox should be checked for that value.
        self.check_test = check_test

    def render(self, name, value, attrs=None):
        html = u'<table class="radioTable"><tr><td><label style="float:left;" for="%(name)s_yes">%(yes_label)s</label><input type="radio" name="%(name)s" \
            id="%(name)s_yes" value="True" ' %({'name':name,'yes_label':ugettext(u'Тийм')}) 
        if value == True or value == u'True' :
            html += u'checked="checked"'
        html += u'/></td><td>&nbsp;&nbsp;&nbsp;</td>'
        html += u'<td><label style="float:left;" for="%(name)s_no">%(no_label)s</label><input type="radio" name="%(name)s" \
            id="%(name)s_no" value="False" ' %({'name':name,'no_label':ugettext(u'Үгүй')})
        if value == False or value == u'False' :
            html += u'checked="checked"'
        html += u'/></td></tr></table>'
        return mark_safe(html)
