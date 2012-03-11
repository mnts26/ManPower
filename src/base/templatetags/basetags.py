#!coding=utf8
from django import template
from django.utils.safestring import mark_safe
from base.models import *

register = template.Library()

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
        html = u'<ul>\n'
        for categ in category_list:
            html += u'<li>\n'
            html += categ.menu_html()
            html += u'</li>\n'
        html += u'</ul>\n'
        return mark_safe(html)
