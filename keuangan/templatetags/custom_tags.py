from django import template
from django.utils.text import slugify

register = template.Library()

@register.filter
def has_key(dict_obj, key):
    if isinstance(dict_obj, dict):
        return key in dict_obj
    return False

@register.filter
def get_item(dict_obj, key):
    if isinstance(dict_obj, dict):
        return dict_obj.get(key)
    return None

@register.filter
def get_range(value):
    return range(1, value + 1)

@register.filter
def to(start, end):
    return range(start, end + 1)

@register.filter
def slugify_text(value):
    return slugify(value)