from django import template

register = template.Library()


# https://www.py4u.net/discuss/143512
@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return qty * unit_price
