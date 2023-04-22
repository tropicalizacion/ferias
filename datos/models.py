from django.db import models
from productos.models import Product

# Create your models here.


class Marketplace(models.Model):
    """Model definition for Marketplace (la feria).

    The "area" field is a PolygonField, which is a special type of field that
    can be used to store a polygon geometry. The PolygonField is a subclass of
    the GeometryField class, which is a subclass of the Field class. This means
    that it can be used in the same way as any other field in Django.
    """
    PROVINCE_CHOICES = [
        (1, 'San José'),
        (2, 'Alajuela'),
        (3, 'Cartago'),
        (4, 'Heredia'),
        (5, 'Guanacaste'),
        (6, 'Puntarenas'),
        (7, 'Limón'),
    ]

    marketplace_id = models.CharField(max_length=50, primary_key=True)
    # General information
    name = models.CharField(max_length=200)
    name_alternate = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    opening_hours = models.CharField(max_length=1023)
    latitude = models.FloatField()
    longitude = models.FloatField()
    area = models.IntegerField(blank=True, null=True) # models.PolygonField(blank=True, null=True)
    size = models.CharField(max_length=1)
    province = models.IntegerField(choices=PROVINCE_CHOICES, blank=False, null=False)
    canton = models.IntegerField(blank=False, null=False)
    district = models.IntegerField(blank=False, null=False)
    address = models.TextField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    operator_committee = models.ManyToManyField('Committee')
    operator_center = models.CharField(max_length=255)
    email = models.EmailField(max_length=63)
    website = models.URLField(max_length=63)
    opening_date = models.DateField()
    # Infrastructure
    fairground = models.BooleanField()
    indoor = models.BooleanField()
    toilets = models.BooleanField()
    parking = models.BooleanField()
    bicycle_parking = models.BooleanField()
    drinking_water = models.BooleanField()
    # Services
    food = models.BooleanField()
    drinks = models.BooleanField()
    handicrafts = models.BooleanField()
    flowers = models.BooleanField()
    plants = models.BooleanField()
    pet_food = models.BooleanField()
    pet_friendly = models.BooleanField()
    # Other
    payment = models.ManyToManyField('Payment')
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.name


class Payment(models.Model):
    """Model definition for Payment."""
    payment_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Committee(models.Model):
    """Model definition for Committee."""
    committee_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
