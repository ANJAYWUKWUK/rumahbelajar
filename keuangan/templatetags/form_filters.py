from django import template

register = template.Library()
 
@register.filter(name='add_class')
def add_class(value, arg):
    """Add CSS classes to form field"""
    return value.as_widget(attrs={'class': arg}) 