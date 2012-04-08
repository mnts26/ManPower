#!coding=utf8
from django import template
from django.utils.safestring import mark_safe
from base.models import *

from django.template import Library, NodeList, Variable, Node, resolve_variable, TemplateSyntaxError, VariableDoesNotExist
from django.contrib.auth.models import Group
from django.utils.encoding import smart_unicode
import datetime, re
register = Library()


register = template.Library()



@register.tag(name="partners")
def partners(parser, token):
    html = ""
    partners = Partners.objects.all()
    

    return htlml 


@register.tag(name="job_category_menu")
def job_category_menu(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return JobCategoryMenuNode()

class JobCategoryMenuNode(template.Node):
    def __init__(self):
        pass
    def render(self, context):
        category_list = JobCategory.objects.filter(parent=None)
        html = u'<ul class="ul-list box">\n'
        for categ in category_list:
            html += u'<li>\n' 
            html += categ.menu_html()#+ u'('+ + u')' 
            html += u'</li>\n'
        html += u'</ul>\n'
        return mark_safe(html)



"""
@param value: Хэлбэржүүлэх тоо
@summary: Тоон тэмдэгт мөрийг мянгатын орны таслалаар хэлбэржүүлнэ.
"""
def filter_digit_format(value):
    if value in (None , 0, '0', '') :
        return '0.00'
    value = value.__str__()
    temdeg = ''
    if value[0] == '-' :
        temdeg = '-'
        value = value[1:]
    result = '';
    if '.' in value :
        left, right = value.split('.')
        right = '.' + right[:2]
    else :
        left = value
        right = ''
    
    i = len(left)-1
    step = 1
    tmp = ''
    while i >= 0 :
        tmp += left[i]
        step += 1
        if i > 0 and step == 4:
            tmp += ','
            step = 1
        i -= 1
        
    i = len(tmp)-1
    while i >= 0 : 
        result += tmp[i]
        i -= 1
    
    result += right
    return temdeg + result

register.filter('digit_format', filter_digit_format)

# -----------------------------------------------------------------------------------------------

"""
@summary: Ажлын урсгалын хүсэлт ирэх үед workitem.activity.description - утгыг засна.
"""
def filter_unsafe_title(value):
    
    value = value[value.find('<h3>')+4: value.find('</h3>')]
    return value
    
register.filter('unsafe_title', filter_unsafe_title)
#------------------------------------------------------------------------------------------------

def filter_unsafe_desc(value):
    
    value = value[value.find('<br/>')+5: len(value)]
    return value
    
register.filter('unsafe_desc', filter_unsafe_desc)

#-------------------------------------------------------------------------------------------------


def HowManyDays(parser, token):
    
    try:
        tag, date = list(token.split_contents())
    except ValueError:
        raise template.TemplateSyntaxError("Tag 'HowManyDays' requires 1 argument.")
    
    return HowManyDaysNode(date)

class HowManyDaysNode(template.Node):
    def __init__(self, date):
        self.date = date
    def render(self, context):
        try :
            date = Variable(self.date).resolve(context)
        except Exception :
            return u'Тодорхойгүй'
        if date == None :
            return u'Тодорхойгүй'
        diff = date - datetime.date.today() 
        d = diff.days
        if d == 0:
            return u'Өнөөдөр'
        elif d < 0:
            return u'<b style="color: #CC2222;">('+ str(abs(d)) +u') хоног</b>'
        else:
            return str(d) +u' хоног'
        
register.tag('howmanydays', HowManyDays)


def do_ifinlist(parser, token, negate):
    bits = list(token.split_contents())
    if len(bits) != 3:
        raise TemplateSyntaxError, "%r takes two arguments" % bits[0]
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return IfInListNode(bits[1], bits[2], nodelist_true, nodelist_false, negate)

def ifinlist(parser, token):
    """
    Given an item and a list, check if the item is in the list

    -----
    item = 'a'
    list = [1, 'b', 'a', 4]
    -----
    {% ifinlist item list %}
        Yup, it's in the list
    {% else %}
        Nope, it's not in the list
    {% endifinlist %}
    """
    return do_ifinlist(parser, token, False)

class IfInListNode(Node):
    def __init__(self, var1, var2, nodelist_true, nodelist_false, negate):
        self.var1, self.var2 = var1, var2
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.negate = negate

    def __repr__(self):
        return "<IfInListNode>"

    def render(self, context):
        try:
            val1 = resolve_variable(self.var1, context)
        except VariableDoesNotExist:
            val1 = None
        try:
            val2 = resolve_variable(self.var2, context)
        except VariableDoesNotExist:
            val2 = None
        if val1 in val2:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)

register.tag('ifinlist', ifinlist)

def do_ifuserhasgroup(parser, token):
    """ Check to see if the currently logged in user belongs to a specific
    group. Requires the Django authentication contrib app and middleware.

    Usage: {% ifuserhasgroup groupname %} ... {% else %} ... {% endifuserhasgroup %}

    """
    bits = list(token.split_contents())
    if len(bits) < 2:
        raise TemplateSyntaxError, "%r required one or greater arguments" % bits[0]
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return IfUserHasGroupNode(bits[1:], nodelist_true, nodelist_false)
    
class IfUserHasGroupNode(Node):
    def __init__(self, list, nodelist_true, nodelist_false):
        self.names = list
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false

    def __repr__(self):
        return "<IfUserHasGroupNode>"

    def render(self, context):
        try :
            user = resolve_variable('user', context)
        except TemplateSyntaxError :
            user = resolve_variable('request', context).user
        
        if not user.is_authenticated:
            return self.nodelist_false.render(context)
        
        names = []
        for name in self.names :
            if name[0] in ("'", '"') and name[0] == name[len(name)-1] :
                name = name[1:len(name)-1]
            names.append(name)
        
        if len(user.groups.filter(name__in=names)) > 0 :
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)

register.tag('ifuserhasgroup', do_ifuserhasgroup)


def do_render_error(parser, token):
    try:
        tag, form = list(token.split_contents())
    except ValueError:
        raise template.TemplateSyntaxError("Tag '%s' requires only 1 argument." %tag)
    
    return RenderErrorNode(form)

class RenderErrorNode(Node):
    def __init__(self, form):
        self.form = form
        
    def render(self, context):
        try :
            form = resolve_variable(self.form, context)
        except TemplateSyntaxError :
            raise template.TemplateSyntaxError("Tag 'render_error' requires valid argument.")
        translate_dic = {u'Enter a number.':u'Тоон утга оруулна уу!', 
                         u'This field is required.': u'Энэ талбарыг бөглөнө үү!',
                         u'Enter a whole number.': u'Бүхэл тоон утга оруулна уу!',
                         u'Enter a valid date/time.': u'Алдаатай байна.!',
                         u'Enter a valid URL.': u'Алдаатай байна.!',
                         u'This URL appears to be a broken link.': u'Веб хаяг ашиглагдахгүй байна.!',
                         u'Enter a valid e-mail address.': u'Зөв хаяг оруулна уу.!',
                         u'Upload a valid image. The file you uploaded was either not an image or a corrupted image.': u'Тохирохгүй зураг оруулсан байна. Зөвхөн jpeg, jpe, jpg төрөлтэй зураг оруулна уу.',
                         u'The submitted file is empty.': u'Таны оруулсан файл хоосон байна.'}
        
        css = '<style type="text/css">'
        css += '.error_list label { color:#CC4422; font-size: 12px; font-weight: bold; }'
        css += '.error_list { color: #CC2222; font-size: 12px; font-weight: normal; }'
        css += '</style>'
        html = '<ul class="error_list">'
        used_error = []
        if type(form) == type([]):
            forms = form
        else :
            forms = [form]
        for form in forms:
            for field in form :
                if field.errors :
                    html += '<li>'
                    first = True
                    for error in field.errors :
                        fmsg = u''
                        if type(error) == unicode :
                            msg = error
                        else :
                            msg = error.__unicode__()
                        if msg == u'This field is required.':
                            fmsg = u'<b>%s</b> талбарыг бөглөнө үү!' % field.label
                        else :
                            if translate_dic.has_key(msg) :
                                fmsg = u'<b>%s</b> - %s ' %(field.label,translate_dic[msg])
                            else :
                                fmsg = u'<b>%s</b> - %s ' %(field.label,msg)
                        if fmsg not in used_error:
                            if not first:
                                fmsg = ', '+fmsg
                            first = False
                            html += fmsg
                            used_error.append(fmsg)
                    html += '</li>\n'
            for error in form.non_field_errors() :
                msg = error
                if type(msg) != unicode :
                    msg = msg.__unicode__()
                if translate_dic.has_key(msg) :
                    html += u'<li>%s</li>\n' %translate_dic[msg]
                else :
                    html += u'<li>%s</li>\n' %msg
        html += '</ul>\n'
        return css + html

register.tag('render_error', do_render_error)

def translate(msg):
    translate_dic = {u'Enter a number.':u'Тоон утга оруулна уу!', 
                         u'This field is required.': u'Энэ талбарыг бөглөнө үү!',
                         u'Enter a whole number.': u'Бүхэл тоон утга оруулна уу!',
                         u'Enter a valid date/time.': u'Алдаатай байна.!',
                         u'Enter a valid URL.': u'Алдаатай байна.!',
                         u'This URL appears to be a broken link.': u'Веб хаяг ашиглагдахгүй байна.!',
                         u'Enter a valid e-mail address.': u'Зөв хаяг оруулна уу.!',
                         u'Upload a valid image. The file you uploaded was either not an image or a corrupted image.': u'Тохирохгүй зураг оруулсан байна. Зөвхөн jpeg, jpe, jpg төрөлтэй зураг оруулна уу.',
                         u'The submitted file is empty.': u'Таны оруулсан файл хоосон байна.'}
    return translate_dic.get(msg, msg)

register.filter('translate', translate)

def do_ifmatch(parser, token):
    """ Check to see if the argument 1 match given pattern (argument 2)
    @param var: str or unicode variable
    @param pattern: regex formated str
    Usage: {% ifmatch var1 \d+{9}. %} ... {% else %} ... {% endifmatch %}
    """
    
    bits = list(token.split_contents())
    if len(bits) != 3:
        raise TemplateSyntaxError, "%r required two arguments" % bits[0]
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return IfMatchNode(bits[1], bits[2], nodelist_true, nodelist_false)

class IfMatchNode(Node):
    def __init__(self, var, regex, nodelist_true, nodelist_false):
        self.var = var
        self.regex = regex
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false

    def __repr__(self):
        return "<IfMatch>"

    def render(self, context):
        try :
            text = resolve_variable(self.var, context)
        except TemplateSyntaxError :
            raise TemplateSyntaxError, u"%r нэртэй хувьсагч байхгүй." % self.var
        
        regex = None
        try :
            regex = re.compile(self.regex)
        except:
            raise TemplateSyntaxError, u"%r текст регуляр илэрхийлэл биш байна. \n\
                Usage: {% ifmatch var1 \d+{9}. %} ... {% else %} ... {% endifmatch %}" % regex
        
        if regex.match(text) :
            return self.nodelist_true.render(context)
        else :
            return self.nodelist_false.render(context) 
        
register.tag('ifmatch', do_ifmatch)



def staff_name(staff_id):
    
    staff = Staff.objects.filter(pk=staff_id)
    if staff :
        return staff[0].first_name + u' '+ staff[0].last_name
    return u''

register.filter('staff_name', staff_name)

