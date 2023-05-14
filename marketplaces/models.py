from django.contrib.gis.db import models
from products.models import Product

# Create your models here.


class Marketplace(models.Model):
    """Model definition for Marketplace (la feria)."""

    SIZE_CHOICES = [
        ("S", "Pequeña"),
        ("M", "Mediana"),
        ("L", "Grande"),
        ("XL", "Muy grande"),
    ]
    BRANCH_CHOICES = [
        ("Atlántico", "Comité Regional Atlántico"),
        ("Brunca", "Comité Regional Brunca"),
        ("Central Central", "Comité Regional Central Central"),
        ("Central Occidental Este", "Comité Regional Central Occidental Este"),
        ("Central Occidental Oeste", "Comité Regional Central Occidental Oeste"),
        ("Central Oriental", "Comité Regional Central Oriental"),
        ("Chorotega", "Comité Regional Chorotega"),
        ("Huetar Norte", "Comité Regional Huetar Norte"),
        ("Pacífico Central", "Comité Regional Pacífico Central"),
    ]
    PARKING_CHOICES = [
        ("lane", "En la calle"),
        ("street_side", "Al lado de la calle en espacio dedicado"),
        ("surface", "En un espacio amplio de parqueo"),
    ]

    marketplace_url = models.CharField(max_length=50, primary_key=True)
    # General information
    name = models.CharField(max_length=127)
    name_alternate = models.CharField(max_length=127, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    opening_hours = models.CharField(max_length=1023, blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=19,
        decimal_places=16,
        help_text="Latitud WGS 84 del centro de la feria.",
    )
    longitude = models.DecimalField(
        max_digits=19,
        decimal_places=16,
        help_text="Latitud WGS 84 del centro de la feria.",
    )
    location = models.PointField(blank=True, null=True)
    area = models.PolygonField(blank=True, null=True)
    size = models.CharField(choices=SIZE_CHOICES, max_length=2, blank=True, null=True)
    province = models.CharField(max_length=31)
    canton = models.CharField(max_length=31)
    district = models.CharField(max_length=31)
    address = models.TextField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=127, blank=True, null=True)
    website = models.URLField(max_length=127, blank=True, null=True)
    opening_date = models.DateField(blank=True, null=True)
    operator = models.CharField(max_length=255, blank=True, null=True)
    branch = models.CharField(
        choices=BRANCH_CHOICES, max_length=63, blank=True, null=True
    )
    # Infrastructure
    parking = models.CharField(
        choices=PARKING_CHOICES, max_length=31, blank=True, null=True
    )
    bicycle_parking = models.BooleanField()
    fairground = models.BooleanField()
    indoor = models.BooleanField()
    toilets = models.BooleanField()
    handwashing = models.BooleanField()
    drinking_water = models.BooleanField()
    # Services
    food = models.BooleanField()
    drinks = models.BooleanField()
    handicrafts = models.BooleanField()
    butcher = models.BooleanField()
    seafood = models.BooleanField()
    garden_centre = models.BooleanField()
    florist = models.BooleanField()
    # Other
    payment = models.ManyToManyField("Payment", blank=True)
    other_services = models.CharField(max_length=255, blank=True, null=True)
    # Products
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    """Model definition for Photo."""

    marketplace = models.ForeignKey(Marketplace, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="marketplaces")
    description = models.CharField(
        max_length=255, blank=True, null=True, help_text="Descripción de la foto (alt)."
    )
    profile = models.BooleanField(default=False)
    cover = models.BooleanField(default=False)

    def __str__(self):
        return self.url


class Payment(models.Model):
    """Model definition for Payment."""

    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name
