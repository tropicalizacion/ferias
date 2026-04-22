from django.contrib import admin
from .models import Tag, BlogPost

admin.site.register(BlogPost)
admin.site.register(Tag)