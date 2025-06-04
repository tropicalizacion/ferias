from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def format_timedelta(duration):
    if not isinstance(duration, timedelta):
        return "No disponible"
    
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    if hours > 0: 
        formatted_time = f"{hours}H {minutes}M"
    else:
        formatted_time = f"{minutes}M"
    
    return formatted_time