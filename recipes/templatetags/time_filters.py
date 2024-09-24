from django import template

register = template.Library()

@register.filter
def format_timedelta(timedelta_obj):
    if isinstance(timedelta_obj, (tuple, list)):
        return "0 minutos"
    
    total_seconds = int(timedelta_obj.total_seconds())
    total_minutes = (total_seconds % 3600)
    
    return f"{total_minutes} minutos" if total_minutes > 0 else "0 minutos"