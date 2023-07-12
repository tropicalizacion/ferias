from django.db import models
from marketplaces.models import Marketplace
from django.contrib.auth.models import User

# Create your models here.


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    until = models.DateTimeField()
    marketplace = models.ManyToManyField(Marketplace)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    publisher = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.title
