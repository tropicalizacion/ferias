from django.contrib import admin
from .models import MarketplaceAdmin, Author

# Register your models here.

admin.site.register(MarketplaceAdmin)
admin.site.register(Author)