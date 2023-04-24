from django.db import models
from products.models import Product

# Create your models here.


class Marketplace(models.Model):
    """Model definition for Marketplace (la feria).
    """
    SIZE_CHOICES = [
        ('S', 'Pequeña'),
        ('M', 'Mediana'),
        ('L', 'Grande'),
        ('XL', 'Muy grande'),
    ]

    PROVINCE_CHOICES = [
        (1, 'San José'),
        (2, 'Alajuela'),
        (3, 'Cartago'),
        (4, 'Heredia'),
        (5, 'Guanacaste'),
        (6, 'Puntarenas'),
        (7, 'Limón'),
    ]

    marketplace_url = models.CharField(max_length=50, primary_key=True)
    # General information
    name = models.CharField(max_length=200)
    name_alternate = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    opening_hours = models.CharField(max_length=1023)
    latitude = models.DecimalField(
        max_digits=20,
        decimal_places=16,
        help_text='Latitud WGS 84 de la feria.')
    longitude = models.DecimalField(
        max_digits=20,
        decimal_places=16,
        help_text='Latitud WGS 84 de la feria.')
    # TODO: area = models.PolygonField(blank=True, null=True)
    area = models.IntegerField(blank=True, null=True)
    size = models.CharField(choices=SIZE_CHOICES, max_length=2)
    province = models.IntegerField(
        choices=PROVINCE_CHOICES, blank=False, null=False)
    canton = models.IntegerField(
        blank=False, null=False,
        help_text='Tres dígitos de código del cantón. Ver https://correos.go.cr/codigo-postal/.')
    district = models.IntegerField(
        blank=False, null=False,
        help_text='Cinco dígitos de código del distrito. Ver https://correos.go.cr/codigo-postal/.')
    address = models.TextField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    operator_committee = models.ForeignKey('Committee',
                                           on_delete=models.SET_NULL,
                                           blank=True, null=True)
    operator = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=63, blank=True, null=True)
    website = models.URLField(max_length=63, blank=True, null=True)
    opening_date = models.DateField(blank=True, null=True)
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
    payment = models.ManyToManyField('Payment', blank=True)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    """Model definition for Payment."""

    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class Committee(models.Model):
    """Model definition for Committee."""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
