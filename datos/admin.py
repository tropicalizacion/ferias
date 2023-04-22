from django.contrib import admin
from .models import Marketplace, Committee, Payment

# Register your models here.

admin.site.register(Marketplace)
admin.site.register(Committee)
admin.site.register(Payment)