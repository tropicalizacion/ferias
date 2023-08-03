from django.contrib.gis import admin
from .models import MarketplaceEdit, PhotoEdit, OpeningHoursEdit, PhoneEdit, EmailEdit, WebsiteEdit

# Register your models here.

admin.site.register(MarketplaceEdit, admin.GISModelAdmin)
admin.site.register(PhotoEdit)
admin.site.register(OpeningHoursEdit)
admin.site.register(PhoneEdit)
admin.site.register(EmailEdit)
admin.site.register(WebsiteEdit)
