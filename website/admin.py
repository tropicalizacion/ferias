from django.contrib import admin
from .models import Announcement, Text, Student

# Register your models here.

admin.site.register(Announcement)
admin.site.register(Text)
admin.site.register(Student)
