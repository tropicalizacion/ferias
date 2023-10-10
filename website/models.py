from django.db import models
from marketplaces.models import Marketplace
from django.contrib.auth.models import User
from django.contrib.gis.db import models
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
    

class District(models.Model):
    postal_code = models.CharField(primary_key=True, max_length=5)
    district = models.CharField(max_length=255)
    n_district = models.IntegerField()
    canton = models.CharField(max_length=255)
    n_canton = models.IntegerField()
    province = models.CharField(max_length=255)
    n_province = models.IntegerField()
    # area = models.MultiPolygonField(srid=4326)
    # population = models.IntegerField()
