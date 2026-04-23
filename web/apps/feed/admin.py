from django.contrib import admin
from .models import Event, News, Alert

# Register your models here.


admin.site.register(Event)
admin.site.register(News)
admin.site.register(Alert)