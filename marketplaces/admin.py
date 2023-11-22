from django.contrib.gis import admin
from .models import Marketplace, Payment, MarketplaceHistory

# Register your models here.

admin.site.register(Marketplace, admin.GISModelAdmin)
admin.site.register(Payment)
admin.site.register(MarketplaceHistory, admin.GISModelAdmin)