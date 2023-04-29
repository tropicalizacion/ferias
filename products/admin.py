from django.contrib import admin
from .models import Product, Variety, Preparation, Storage

# Register your models here.

admin.site.register(Product)
admin.site.register(Variety)
admin.site.register(Preparation)
admin.site.register(Storage)
