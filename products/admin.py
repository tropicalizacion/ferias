from django.contrib.gis import admin
from .models import Product, Variety, Preparation, Storage, Origin

# Register your models here.

admin.site.register(Product)
admin.site.register(Variety)
admin.site.register(Preparation)
admin.site.register(Storage)
admin.site.register(Origin, admin.GISModelAdmin)
