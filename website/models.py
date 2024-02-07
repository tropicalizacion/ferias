from django.db import models
from marketplaces.models import Marketplace
from django.contrib.auth.models import User
from datetime import date
from django.utils.timezone import now

# Create your models here.


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateField()
    until = models.DateField()
    marketplace = models.ForeignKey(Marketplace, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    publisher = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Text(models.Model):
    page = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return f"{self.page}: {self.section}"


class Student(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    career = models.CharField(max_length=100)
    work = models.TextField()
    factor = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} {self.last_name}"