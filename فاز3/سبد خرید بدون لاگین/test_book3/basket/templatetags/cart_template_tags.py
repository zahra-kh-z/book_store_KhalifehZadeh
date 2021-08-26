from django import template
from basket.models import *

register = template.Library()


@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    return qty * unit_price