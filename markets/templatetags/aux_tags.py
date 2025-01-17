from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
import markdown

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(escape(text), extensions=['tables', 'def_list']))
