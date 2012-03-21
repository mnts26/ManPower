#coding:utf-8
"""
@copyright: Jacara
@contact: baskhuujacara@gmail.com; baskhuu@usi.mn
@summary: Tools of usi extensions
"""
from usiextensions.widgets import *
from django.utils.translation import ugettext_lazy as _
from django.forms.fields import *
from django.forms.widgets import *
from django.forms.util import ErrorList, ValidationError
from django.utils.encoding import smart_unicode
import datetime
import time

EMPTY_VALUES = (None, '')

class extDateField(DateField):
    widget = extDateWidget
    default_error_messages = {
        'invalid': u'Зөв огноо оруулна уу!',
    }
    
    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        super(extDateField, self).__init__(*args, **kwargs)
        widget = extDateWidget
        if isinstance(widget, type):
            widget = widget()

        # Trigger the localization machinery if needed.
        if self.localize:
            widget.is_localized = True

        # Let the widget know whether it should display as required.
        widget.is_required = self.required

        # Hook into self.widget_attrs() for any Field-specific HTML attributes.
        extra_attrs = self.widget_attrs(widget)
        if extra_attrs:
            widget.attrs.update(extra_attrs)

        self.widget = widget
    
class extTimeField(forms.TimeField):
    widget = extTimeWidget
    default_error_messages = {
        'invalid': _(u'Enter a valid time.'),
        'required': _(u'This field is required.'),
    }

    def __init__(self, input_formats=None, *args, **kwargs):
        super(extTimeField, self).__init__(input_formats, *args, **kwargs)
#        self.input_formats = input_formats or DEFAULT_TIME_INPUT_FORMATS

    def clean(self, value):
        """
        Validates that the input can be converted to a time. Returns a Python
        datetime.time object.
        """
        super(TimeField, self).clean(value)
        if value in EMPTY_VALUES:
            return None
        if isinstance(value, datetime.time):
            return value
        for format in self.input_formats:
            try:
                return datetime.time(*time.strptime(value, format)[3:6])
            except ValueError:
                continue
        raise ValidationError(self.error_messages['invalid'])

class extCharField(CharField):
    widget = extTextInput
#    default_error_messages = {
#        'max_length'    : _(u'Тэмдэгтийн дээд хэмжээ %(max)d байх ёстой (%(length)d урттай оруулсан байна)!'),
#        'min_length'    : _(u'Тэмдэгтийн доод хэмжээ %(min)d байх ёстой (%(length)d урттай оруулсан байна)!'),
#        'required'      : _(u'Энэ талбарыг бөглөх шаардлагатай!'),
#        'invalid'       : _(u'Тохирох утга оруулна уу!'),
#    }
    default_error_messages = {
        'max_length': _(u'Ensure this value has at most %(max)d characters (it has %(length)d).'),
        'min_length': _(u'Ensure this value has at least %(min)d characters (it has %(length)d).'),
        'required': _(u'This field is required.'),
        'invalid': _(u'Enter a valid value.'),
    }
    
    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        super(extCharField, self).__init__(*args, **kwargs)
    
    def widget_attrs(self, widget):
        if self.max_length is not None and isinstance(widget, (extTextInput, extPasswordInput)):
            # The HTML attribute is maxlength, not max_length.
            return {'maxlength': str(self.max_length)}

class extIntegerField(IntegerField) :
    widget = extIntegerWidget
#    default_error_messages = {
#        'invalid'       : _(u'Бүхэл тоон утга оруулна уу!'),
#        'max_value'     : _(u'%s-с бага буюу тэнцүү утга оруулна уу!'),
#        'min_value'     : _(u'%s-с их буюу тэнцүү утга оруулна уу!'),
#        'required'      : _(u'Энэ талбарыг бөглөх шаардлагатай!'),
#    }
    default_error_messages = {
        'invalid': _(u'Enter a whole number.'),
        'max_value': _(u'Ensure this value is less than or equal to %s.'),
        'min_value': _(u'Ensure this value is greater than or equal to %s.'),
        'required': _(u'This field is required.'),
    }
    
    def __init__(self, max_value=None, min_value=None, *args, **kwargs):
        self.max_value, self.min_value = max_value, min_value
        super(extIntegerField, self).__init__(*args, **kwargs)


class extFloatField(FloatField) :
    widget = extDecimalWidget
#    default_error_messages = {
#        'invalid'       : _(u'Тоон утга оруулна уу!'),
#        'max_value'     : _(u'%s-с бага буюу тэнцүү утга оруулна уу!'),
#        'min_value'     : _(u'%s-с их буюу тэнцүү утга оруулна уу!'),
#    }
    default_error_messages = {
        'invalid': _(u'Enter a number.'),
        'max_value': _(u'Ensure this value is less than or equal to %s.'),
        'min_value': _(u'Ensure this value is greater than or equal to %s.'),
    }
    
    def __init__(self, max_value=None, min_value=None, *args, **kwargs):
        self.max_value, self.min_value = max_value, min_value
        super(extFloatField, self).__init__(self, *args, **kwargs)

class extDecimalField(DecimalField) :
#    default_error_messages = {
#        'invalid'             : _(u'Тоон утга оруулна уу!'),
#        'max_value'           : _(u'%s-с бага буюу тэнцүү утга оруулна уу!'),
#        'min_value'           : _(u'%s-с их буюу тэнцүү утга оруулна уу!'),
#        'max_digits'          : _(u'Тоон утга дээд тал нь %s оронтой байх ёстой!'),
#        'max_decimal_places'  : _(u'Бутархай хэсэг дээд тал нь %s оронтой байх ёстой!'),
#        'max_whole_digits'    : _(u'Бүхэл хэсэг дээд тал нь %s оронтой байх ёстой!')
#    }
    default_error_messages = {
        'invalid': _(u'Enter a number.'),
        'max_value': _(u'Ensure this value is less than or equal to %s.'),
        'min_value': _(u'Ensure this value is greater than or equal to %s.'),
        'max_digits': _('Ensure that there are no more than %s digits in total.'),
        'max_decimal_places': _('Ensure that there are no more than %s decimal places.'),
        'max_whole_digits': _('Ensure that there are no more than %s digits before the decimal point.')
    }

    def __init__(self, max_value=None, min_value=None, max_digits=None, decimal_places=None, *args, **kwargs):
        self.max_value, self.min_value = max_value, min_value
        self.max_digits, self.decimal_places = max_digits, decimal_places
        super(extDecimalField, self).__init__(self, *args, **kwargs)

class extChoiceField(forms.ChoiceField):
    widget = extSelect
    default_error_messages = {
        'invalid_choice': _(u'Select a valid choice. %(value)s is not one of the available choices.'),
    }

#    def __init__(self, choices=(), required=True, widget=None, label=None,
#                 initial=None, help_text=None, *args, **kwargs):
#        super(extChoiceField, self).__init__(choices, required, widget, label, initial,
#                                          help_text, *args, **kwargs)
#
#    def _get_choices(self):
#        return self._choices
#
#    def _set_choices(self, value):
#        # Setting choices also sets the choices on the widget.
#        # choices can be any iterable, but we call list() on it because
#        # it will be consumed more than once.
#        self._choices = self.widget.choices = list(value)
#
#    choices = property(_get_choices, _set_choices)
#
#    def clean(self, value):
#        """
#        Validates that the input is in self.choices.
#        """
#        value = super(ChoiceField, self).clean(value)
#        if value in EMPTY_VALUES:
#            value = u''
#        value = smart_unicode(value)
#        if value == u'':
#            return value
#        if not self.valid_value(value):
#            raise ValidationError(self.error_messages['invalid_choice'] % {'value': value})
#        return value
#
#    def valid_value(self, value):
#        "Check to see if the provided value is a valid choice"
#        for k, v in self.choices:
#            if type(v) in (tuple, list):
#                # This is an optgroup, so look inside the group for options
#                for k2, v2 in v:
#                    if value == smart_unicode(k2):
#                        return True
#            else:
#                if value == smart_unicode(k):
#                    return True
#        return False

class extModelChoiceField(forms.ChoiceField) :
    widget = extModelSelect
    default_error_messages = {
        'invalid_choice': _(u'Select a valid choice. %(value)s is not one of the available choices.'),
        # Зөв утга сонгоно уу. %(value)s буруу сонголт байна.
    }

    def __init__(self, model=None, search=None, display=None, required=True, 
                 label=None, initial=None, help_text=None, error_messages=None, show_hidden_initial=False):
        
        if label is not None:
            label = smart_unicode(label)
        self.required, self.label, self.initial = required, label, initial
        self.show_hidden_initial = show_hidden_initial
        if help_text is None:
            self.help_text = u''
        else:
            self.help_text = smart_unicode(help_text)
        
        self.widget = extModelSelect(attrs={'model':model,'search':search,'display':display})
        self.model = model

        # Increase the creation counter, and save our local copy.
        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

        def set_class_error_messages(messages, klass):
            for base_class in klass.__bases__:
                set_class_error_messages(messages, base_class)
            messages.update(getattr(klass, 'default_error_messages', {}))

        messages = {}
        set_class_error_messages(messages, self.__class__)
        messages.update(error_messages or {})
        self.error_messages = messages
    
    def super_clean(self, value):
        if self.required and value in EMPTY_VALUES :
            raise ValidationError(self.error_messages['required'])
        return value

    def clean(self, value):
        """
        Validates that the input is in self.choices.
        """
        value = self.super_clean(value)
        if value in EMPTY_VALUES :
            value = u''
        value = smart_unicode(value)
        if value == u'':
            return value
        value_obj = self.valid_value(value)
        if not value_obj :
            raise ValidationError(self.error_messages['invalid_choice'] % {'value': value})
        return value_obj

    def valid_value(self, value):
        "Check to see if the provided value is a valid choice"
        try :
            obj = self.model.objects.get(pk=value)
        except :
            return False
        return obj
    
class extBooleanField(forms.Field):
    widget = extBooleanInput
    
    def clean(self, value):
        """Returns a Python boolean object."""
        # Explicitly check for the string 'False', which is what a hidden field
        # will submit for False. Because bool("True") == True, we don't need to
        # handle that explicitly.
        if value == 'False':
            value = False
        else:
            value = bool(value)
        super(extBooleanField, self).clean(value)
        if not value and self.required:
            raise ValidationError(self.error_messages['required'])
        return value
    
class extNullBooleanField(forms.Field):
    """
    A field whose valid values are None, True and False. Invalid values are
    cleaned to None.
    """
    widget = extNullBooleanSelect

    def clean(self, value):
        """
        Explicitly checks for the string 'True' and 'False', which is what a
        hidden field will submit for True and False. Unlike the
        Booleanfield we also need to check for True, because we are not using
        the bool() function
        """
        if value in (True, 'True'):
            return True
        elif value in (False, 'False'):
            return False
        else:
            return None