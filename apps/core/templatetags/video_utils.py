from django import template
from django.template.defaultfilters import stringfilter
import re


register = template.Library()


@register.filter
@stringfilter
def simplify(value):
    replaced = re.sub(' - Audiência Pública .*', '', value)
    return replaced
