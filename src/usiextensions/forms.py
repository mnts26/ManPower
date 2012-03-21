#coding:utf-8
"""
@copyright: Jacara
@contact: baskhuujacara@gmail.com; baskhuu@usi.mn
@summary: Forms of usi extensions
"""
from copy import deepcopy
from django import forms
from usiextensions.fields import *
from django.forms.util import flatatt, ErrorDict, ErrorList, ValidationError
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import StrAndUnicode, smart_unicode, force_unicode
from django.forms.models import model_to_dict, save_instance
from django.utils.datastructures import SortedDict
from django.forms.widgets import Media, media_property, TextInput, Textarea

def ext_update_fields(fields) :
    ''' django ын стандарт field үүдийг тодорхойлсон байвал
        өргөтгөсөн field ээр солих
    '''
    ext_fields = {}
    for name, field in fields.items() :
        widget = field.widget
        if isinstance(widget, forms.TextInput) : widget = None
        if isinstance(widget, forms.Textarea) : widget = extTextarea(widget.attrs)
        if isinstance(widget, forms.PasswordInput) : widget = extPasswordInput(widget.attrs)
        if isinstance(widget, forms.Select) : field.widget = extSelect(widget.attrs, widget.choices)
        if isinstance(widget, forms.CheckboxInput) : field.widget = extBooleanInput()
        
        if field.__class__.__name__ in ('CharField','EmailField','RegexField') :
            ext_fields[name] = extCharField(field.max_length, field.min_length,
                    required=field.required, widget=widget, label=field.label,
                    initial=field.initial, help_text=field.help_text,
                    error_messages=field.error_messages, show_hidden_initial=field.show_hidden_initial)
        elif field.__class__.__name__ == 'DateField' :
            ext_fields[name] = extDateField(required=field.required, widget=widget, label=field.label,
                    initial=field.initial, help_text=field.help_text,
                    error_messages=field.error_messages, show_hidden_initial=field.show_hidden_initial)
        elif field.__class__.__name__ == 'TimeField' :
            ext_fields[name] = extTimeField(required=field.required, widget=None, label=field.label,
                    initial=field.initial, help_text=field.help_text,
                    error_messages=field.error_messages, show_hidden_initial=field.show_hidden_initial)
        elif field.__class__.__name__ ==  'ComboField' :
            ext_fields[name] = extComboField(fields=field.fields, required=field.required, widget=widget, label=field.label,
                    initial=field.initial, help_text=field.help_text,
                    error_messages=field.error_messages, show_hidden_initial=field.show_hidden_initial)
        elif field.__class__.__name__ == 'NullBooleanField' :
            ext_fields[name] = extNullBooleanField(required=field.required, widget=None, label=field.label,
                    initial=field.initial, help_text=field.help_text,
                    error_messages=field.error_messages, show_hidden_initial=field.show_hidden_initial)
        elif field.__class__.__name__ == 'BooleanField' :
            ext_fields[name] = extBooleanField(required=field.required, widget=None, label=field.label,
                    initial=field.initial, help_text=field.help_text,
                    error_messages=field.error_messages, show_hidden_initial=field.show_hidden_initial)
        else :
            ext_fields[name] = field
    return ext_fields

class extDeclarativeFieldsMetaclass(type):
    """
    Metaclass that converts Field attributes to a dictionary called
    'base_fields', taking into account parent class 'base_fields' as well.
    """
    def __new__(cls, name, bases, attrs):
        attrs['base_fields'] = ext_update_fields(forms.forms.get_declared_fields(bases, attrs))
        new_class = super(extDeclarativeFieldsMetaclass,
                     cls).__new__(cls, name, bases, attrs)
        if 'media' not in attrs:
            new_class.media = media_property(new_class)
        return new_class

class extBaseForm(forms.BaseForm) :
    
    def _html_output(self, normal_row, error_row, row_ender, 
                     help_text_html, title_start_row, title_end_row,
                     errors_on_separate_row):
        print 'called _html_output'
        "Helper function for outputting HTML. Used by as_table(), as_ul(), as_p()."
        top_errors = self.non_field_errors() # Errors that should be displayed above all fields.
        output, hidden_fields = [], []
        sequence = []
        if hasattr(self, '_meta') :
            sequence = getattr(self._meta, 'sequence', None)
        names = self.fields.keys()
        sortednames = []
        data = {}
        fields = []
        if sequence :
            for seq in sequence :
                if isinstance(seq, tuple) :
                    fields.append(u'%s.__start'%seq[0])
                    if not isinstance(seq[1], list) :
                        raise Exception(u'%s form-ын sequence буруу байна.'%self._meta.__class__)
                    for f in seq[1] :
                        if f in names :
                            fields.append(f)
                    fields.append('__end')
                elif isinstance(seq, str) and seq in names :
                    fields.append(seq)
                else :
                    raise Exception(u'%s form-ын sequence буруу байна.'%self._meta.__class__)
        for name in names :
            if not name in fields :
                fields.append(name)
        
        for name in fields :
            if '.__start' in name :
                title = name[:name.find('.__start')]
                output.append(title_start_row % {'title':title})
                continue
            elif '__end' == name :
                output.append(title_end_row)
                continue
            field = self.fields[name]
            bf = forms.forms.BoundField(self, field, name)
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors]) # Escape and cache in local variable.
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend([u'(Hidden field %s) %s' % (name, force_unicode(e)) for e in bf_errors])
                hidden_fields.append(unicode(bf))
            else :
                error_class = u''
                errors = u''
                if bf_errors :
                    if errors_on_separate_row :
                        errors = force_unicode(bf_errors)
                    else :
                        output.append(error_row % force_unicode(bf_errors))
                    error_class = u'error'
                
                label = u''
                if bf.label :
                    label += conditional_escape(force_unicode(bf.label))
                    # Only add the suffix if the label does not end in
                    # punctuation.
                    
                    if self.label_suffix :
                        if label[-1] not in ':?.!':
                            label += u' '+self.label_suffix
                    if field.required :
                        label += u'<strong> *</strong>'
                    label = bf.label_tag(label) or ''
                
                if field.help_text :
                    help_text = help_text_html % force_unicode(field.help_text)
                else :
                    help_text = u''
                output.append(normal_row % {'errors': force_unicode(errors), 'label': force_unicode(label), 
                                            'field': unicode(bf), 'help_text': help_text, 'error_class':error_class})
        if top_errors:
            output.insert(0, error_row % force_unicode(top_errors))
        if hidden_fields: # Insert any hidden fields in the last row.
            str_hidden = u''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = normal_row % {'errors': '', 'label': '', 'field': '', 'help_text': ''}
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return u'\n'.join(output)
    
    def as_table(self) :
        print 'called as_table'
        "Returns this form rendered as HTML <tr>s -- excluding the <table></table>."
        normal_row = u'<tr class="%(error_class)s"><td class="label">%(label)s</td><td>%(field)s%(help_text)s%(errors)s</td></tr>'
        error_row = u'<tr><td colspan="2">%s</td></tr>'
        row_ender = u'</td></tr>'
        help_text_html = u'<br/>%s'
        title_start_row = u'<tr><td colspan="2" class="extFormTableTitle">%(title)s</td></tr>'
        title_end_row = u'<tr><td colspan="2" class="extFormTableTitleEnd"> </td></tr>'
        errors_on_separate_row = True
        
        return mark_safe(u'<table class="extFormTable">' + 
                self._html_output(normal_row, error_row, row_ender, help_text_html, title_start_row, title_end_row, errors_on_separate_row)
                + u'</table>'
        )

    def as_ul(self) :
        "Returns this form rendered as HTML <li>s -- excluding the <ul></ul>."
        return mark_safe(u'ul class="extFormUL"'+self._html_output(u'<li>%(errors)s%(label)s %(field)s%(help_text)s</li>', 
                u'<li>%s</li>', '</li>', u' %s', True)+u'</ul>')

    def as_p(self) :
        "Returns this form rendered as HTML <p>s."
        return mark_safe(self._html_output(u'<p>%(label)s %(field)s%(help_text)s</p>', u'%s', '</p>', u' %s', True))

class extModelFormOptions(forms.models.ModelFormOptions) :
    
    def __init__(self, options=None) :
        self.sequence = getattr(options, 'sequence', [])
        super(extModelFormOptions, self).__init__(options=options)

class extModelFormMetaclass(forms.models.ModelFormMetaclass) :
    
    def __new__(cls, name, bases, attrs) :
        formfield_callback = attrs.pop('formfield_callback',
                lambda f: f.formfield())
        try:
            parents = [b for b in bases if issubclass(b, extBaseModelForm)]
        except NameError, e :
            raise Exception('name error usiextensions.forms.py line 197 : ',e)
            # We are defining ModelForm itself.
            parents = None
        declared_fields = forms.forms.get_declared_fields(bases, attrs, False)
        new_class = super(extModelFormMetaclass, cls).__new__(cls, name, bases, attrs)
        if not parents :
            return new_class

        if 'media' not in attrs :
            new_class.media = forms.widgets.media_property(new_class)
        opts = new_class._meta = extModelFormOptions(getattr(new_class, 'Meta', None))
        if opts.model :
            # If a model is defined, extract form fields from it.
            fields = forms.models.fields_for_model(opts.model, opts.fields,
                                      opts.exclude, formfield_callback=formfield_callback)
            
            # Override default model fields with any custom declared ones
            # (plus, include all the other declared fields).
            fields.update(declared_fields)
        else :
            fields = declared_fields
        new_class.declared_fields = ext_update_fields(declared_fields)
        new_class.base_fields = ext_update_fields(fields)
        return new_class

class extBaseModelForm(extBaseForm):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
        opts = self._meta
        if instance is None:
            # if we didn't get an instance, instantiate a new one
            self.instance = opts.model()
            object_data = {}
        else:
            self.instance = instance
            object_data = model_to_dict(instance, opts.fields, opts.exclude)
        # if initial was provided, it should override the values from instance
        if initial is not None:
            object_data.update(initial)
        super(extBaseModelForm, self).__init__(data, files, auto_id, prefix, object_data,
                                            error_class, label_suffix, empty_permitted)
    def clean(self):
        self.validate_unique()
        return self.cleaned_data

    def validate_unique(self):
        from django.db.models.fields import FieldDoesNotExist

        # Gather a list of checks to perform. Since this is a ModelForm, some
        # fields may have been excluded; we can't perform a unique check on a
        # form that is missing fields involved in that check.
        unique_checks = []
        for check in self.instance._meta.unique_together[:]:
            fields_on_form = [field for field in check if field in self.fields]
            if len(fields_on_form) == len(check):
                unique_checks.append(check)
            
        form_errors = []
        
        # Gather a list of checks for fields declared as unique and add them to
        # the list of checks. Again, skip fields not on the form.
        for name, field in self.fields.items():
            try:
                f = self.instance._meta.get_field_by_name(name)[0]
            except FieldDoesNotExist:
                # This is an extra field that's not on the ModelForm, ignore it
                continue
            # MySQL can't handle ... WHERE pk IS NULL, so make sure we
            # don't generate queries of that form.
            is_null_pk = f.primary_key and self.cleaned_data[name] is None
            if name in self.cleaned_data and f.unique and not is_null_pk:
                unique_checks.append((name,))
                
        # Don't run unique checks on fields that already have an error.
        unique_checks = [check for check in unique_checks if not [x in self._errors for x in check if x in self._errors]]
        
        for unique_check in unique_checks:
            # Try to look up an existing object with the same values as this
            # object's values for all the unique field.
            
            lookup_kwargs = {}
            for field_name in unique_check:
                lookup_kwargs[field_name] = self.cleaned_data[field_name]
            
            qs = self.instance.__class__._default_manager.filter(**lookup_kwargs)

            # Exclude the current object from the query if we are editing an 
            # instance (as opposed to creating a new one)
            if self.instance.pk is not None:
                qs = qs.exclude(pk=self.instance.pk)
                
            # This cute trick with extra/values is the most efficient way to
            # tell if a particular query returns any results.
            if qs.extra(select={'a': 1}).values('a').order_by():
                model_name = capfirst(self.instance._meta.verbose_name)
                
                # A unique field
                if len(unique_check) == 1:
                    field_name = unique_check[0]
                    field_label = self.fields[field_name].label
                    # Insert the error into the error dict, very sneaky
                    self._errors[field_name] = ErrorList([
                        _(u"%(model_name)s with this %(field_label)s already exists.") % \
                        {'model_name': unicode(model_name),
                         'field_label': unicode(field_label)}
                    ])
                # unique_together
                else:
                    field_labels = [self.fields[field_name].label for field_name in unique_check]
                    field_labels = get_text_list(field_labels, _('and'))
                    form_errors.append(
                        _(u"%(model_name)s with this %(field_label)s already exists.") % \
                        {'model_name': unicode(model_name),
                         'field_label': unicode(field_labels)}
                    )
                
                # Remove the data from the cleaned_data dict since it was invalid
                for field_name in unique_check:
                    del self.cleaned_data[field_name]
        
        if form_errors:
            # Raise the unique together errors since they are considered form-wide.
            raise ValidationError(form_errors)

    def save(self, commit=True):
        """
        Saves this ``form``'s cleaned_data into model instance
        ``self.instance``.

        If commit=True, then the changes to ``instance`` will be saved to the
        database. Returns ``instance``.
        """
        if self.instance.pk is None:
            fail_message = 'created'
        else:
            fail_message = 'changed'
        return save_instance(self, self.instance, self._meta.fields, fail_message, commit)

class extModelForm(extBaseModelForm):
    
    __metaclass__ = extModelFormMetaclass

class extForm(extBaseForm):
    
    __metaclass__ = extDeclarativeFieldsMetaclass