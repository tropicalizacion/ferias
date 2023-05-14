from django.contrib.gis import admin
from .models import Marketplace, Payment

# Register your models here.

admin.site.register(Marketplace, admin.GISModelAdmin)
admin.site.register(Payment)