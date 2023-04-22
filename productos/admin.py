from django.contrib import admin
from .models import Product, Preparation, Storage

# Register your models here.

admin.site.register(Product)
admin.site.register(Preparation)
admin.site.register(Storage)