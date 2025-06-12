from django import template

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
