from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Split a string by the given argument"""
    return value.split(arg)

@register.filter
def strip(value):
    """Strip whitespace from a string"""
    return value.strip()
