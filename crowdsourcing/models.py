from django.contrib.gis.db import models
from products.models import Product
from marketplaces.models import Marketplace, Payment
from django.contrib.auth.models import User

# Create your models here.


class MarketplaceEdit(models.Model):
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
        ("lane", "en la calle"),
        ("street_side", "al lado de la calle en espacio dedicado"),
        ("surface", "un espacio amplio de parqueo"),
    ]
    FEATURE_CHOICES = [
        ("T", "Sí"),
        ("F", "No"),
        ("U", "Desconocido"),
    ]

    marketplace_edit_id = models.AutoField(primary_key=True)
    marketplace = models.ForeignKey(Marketplace, on_delete=models.CASCADE)
    # General information
    name = models.CharField(max_length=127)
    name_alternate = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    opening_date = models.DateField(blank=True, null=True)
    location = models.PointField(blank=True, null=True)
    area = models.PolygonField(blank=True, null=True)
    province = models.CharField(max_length=31, blank=True, null=True)
    canton = models.CharField(max_length=31, blank=True, null=True)
    district = models.CharField(max_length=31, blank=True, null=True)
    postal_code = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    size = models.CharField(choices=SIZE_CHOICES, max_length=2, blank=True, null=True)
    operator = models.CharField(max_length=255, blank=True, null=True)
    branch = models.CharField(
        choices=BRANCH_CHOICES, max_length=63, blank=True, null=True
    )
    # Infrastructure
    parking = models.BooleanField(default=None, blank=True, null=True)
    bicycle_parking = models.BooleanField(default=None, blank=True, null=True)
    fairground = models.BooleanField(default=None, blank=True, null=True)
    indoor = models.BooleanField(default=None, blank=True, null=True)
    toilets = models.BooleanField(default=None, blank=True, null=True)
    handwashing = models.BooleanField(default=None, blank=True, null=True)
    drinking_water = models.BooleanField(default=None, blank=True, null=True)
    # Services
    food = models.BooleanField(default=None, blank=True, null=True)
    drinks = models.BooleanField(default=None, blank=True, null=True)
    handicrafts = models.BooleanField(default=None, blank=True, null=True)
    butcher = models.BooleanField(default=None, blank=True, null=True)
    dairy = models.BooleanField(default=None, blank=True, null=True)
    seafood = models.BooleanField(default=None, blank=True, null=True)
    garden_centre = models.BooleanField(default=None, blank=True, null=True)
    florist = models.BooleanField(default=None, blank=True, null=True)
    # Other
    payment = models.ManyToManyField(Payment, blank=True)
    # Products
    products = models.ManyToManyField(Product, blank=True)
    # Crowdsourcing-specific fields
    comments = models.TextField(blank=True, null=True)
    submitted_by = models.CharField(max_length=127, blank=True, null=True)
    submitted_on = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.marketplace} ({self.submitted_on})"


class MarketplaceProductsEdit(models.Model):
    """Model definition for MarketplaceProducts."""

    marketplace = models.ForeignKey(Marketplace, on_delete=models.CASCADE)
    varieties = models.JSONField(blank=True, null=True)
    submitted_by = models.CharField(max_length=127, blank=True, null=True)
    is_reviewed = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.marketplace}"


class PhotoEdit(models.Model):
    """Model definition for Photo."""

    marketplace = models.ForeignKey(MarketplaceEdit, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="crowdsourcing")
    description = models.CharField(
        max_length=255, blank=True, null=True, help_text="Descripción de la foto."
    )
    alt = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.url}: {self.description}"


class OpeningHoursEdit(models.Model):
    DAY_CHOICES = [
        ("Mo", "Lunes"),
        ("Tu", "Martes"),
        ("We", "Miércoles"),
        ("Th", "Jueves"),
        ("Fr", "Viernes"),
        ("Sa", "Sábado"),
        ("Su", "Domingo"),
    ]

    marketplace = models.ForeignKey(Marketplace, on_delete=models.CASCADE)
    marketplace_edit_id = models.ForeignKey("MarketplaceEdit", on_delete=models.CASCADE)
    day_opens = models.CharField(
        choices=DAY_CHOICES, max_length=2, blank=True, null=True
    )
    hour_opens = models.TimeField(blank=True, null=True)
    day_closes = models.CharField(
        choices=DAY_CHOICES, max_length=2, blank=True, null=True
    )
    hour_closes = models.TimeField(blank=True, null=True)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.marketplace}: {self.day_opens} {self.hour_opens} - {self.hour_closes}"


class PhoneEdit(models.Model):
    """Model definition for Phone."""

    marketplace = models.ForeignKey(Marketplace, on_delete=models.CASCADE)
    marketplace_edit_id = models.ForeignKey("MarketplaceEdit", on_delete=models.CASCADE)
    phone = models.TextField(max_length=31, blank=True, null=True)
    type = models.CharField(max_length=31, blank=True, null=True)
    is_reviewed = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.marketplace} ({self.marketplace_edit_id.submitted_on})"


class EmailEdit(models.Model):
    """Model definition for Email."""

    marketplace = models.ForeignKey(Marketplace, on_delete=models.CASCADE)
    marketplace_edit_id = models.ForeignKey("MarketplaceEdit", on_delete=models.CASCADE)
    email = models.EmailField(max_length=127, blank=True, null=True)
    type = models.CharField(max_length=31, blank=True, null=True)
    is_reviewed = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.marketplace} ({self.marketplace_edit_id.submitted_on})"


class WebsiteEdit(models.Model):
    """Model definition for Website."""

    marketplace = models.ForeignKey(Marketplace, on_delete=models.CASCADE)
    marketplace_edit_id = models.ForeignKey("MarketplaceEdit", on_delete=models.CASCADE)
    website = models.URLField(max_length=127, blank=True, null=True)
    type = models.CharField(max_length=31, blank=True, null=True)
    is_reviewed = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.marketplace} ({self.marketplace_edit_id.submitted_on})"
