from django.contrib.gis import admin
from .models import MarketplaceEdit, PhotoEdit, OpeningHoursEdit

# Register your models here.

admin.site.register(MarketplaceEdit, admin.GISModelAdmin)
admin.site.register(PhotoEdit)
admin.site.register(OpeningHoursEdit)
