from django.contrib.gis.db import models

# Create your models here.


class Product(models.Model):
    """Model definition for Product."""

    CATEGORY_CHOICES = [
        (1, "cereales"),
        (2, "legumbres"),
        (3, "frutas"),
        (4, "hortalizas"),
        (5, "condimentos")
    ]

    CENTER_ORIGIN_CHOICES = [
        (1, "(I) Asia oriental"),
        (2, "(II) Subcontinente indio"),
        (3, "(IIa) Archipiélago indo-malayo"),
        (4, "(III) Sureste y centro de Asia"),
        (5, "(IV) Asia Menor y Creciente Fértil"),
        (6, "(V) Mediterráneo"),
        (7, "(VI) Abisinia (actual Etiopía)"),
        (8, "(VII) Mesoamérica"),
        (9, "(VIII) Región andina tropical"),
        (10, "(VIIIa) Región chilena"),
        (11, "(VIIIb) Región brasileña-paraguaya"),
    ]

    SEASON_CHOICES = [
        (0, "imposible o muy difícil de encontrar el producto"),
        (1, "producto escaso"),
        (2, "producto abundante"),
        (3, "plena temporada de cosecha"),
    ]

    product_id = models.AutoField(primary_key=True)
    product_url = models.CharField(max_length=63, blank=False, null=False)
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    scientific_name = models.CharField(max_length=63, blank=False, null=False)
    scientific_name_variety = models.CharField(max_length=127, blank=True, null=True)
    common_name = models.CharField(max_length=63, blank=False, null=False)
    common_name_variety = models.CharField(max_length=127, blank=True, null=True)
    common_name_alternate = models.CharField(max_length=127, blank=True, null=True)
    image = models.ImageField(upload_to="images", blank=True, null=True)
    icon = models.FileField(upload_to="icons", blank=True, null=True)
    center_origin = models.IntegerField(choices=CENTER_ORIGIN_CHOICES)
    jan = models.IntegerField(choices=SEASON_CHOICES, blank=True, null=True)
    feb = models.IntegerField(choices=SEASON_CHOICES, blank=True, null=True)
    mar = models.IntegerField(choices=SEASON_CHOICES, blank=True, null=True)
    apr = models.IntegerField(choices=SEASON_CHOICES, blank=True, null=True)
    may = models.IntegerField(choices=SEASON_CHOICES, blank=True, null=True)
    jun = models.IntegerField(choices=SEASON_CHOICES, blank=True, null=True)
    jul = models.IntegerField(choices=SEASON_CHOICES, blank=True, null=True)
    aug = models.IntegerField(choices=SEASON_CHOICES, blank=True, null=True)
    sep = models.IntegerField(choices=SEASON_CHOICES, blank=True, null=True)
    oct = models.IntegerField(choices=SEASON_CHOICES, blank=True, null=True)
    nov = models.IntegerField(choices=SEASON_CHOICES, blank=True, null=True)
    dec = models.IntegerField(choices=SEASON_CHOICES, blank=True, null=True)
    nutritional_description = models.TextField(max_length=127, blank=True, null=True)

    def __str__(self):
        return self.common_name


class Preparation(models.Model):
    """Model definition for Preparation."""

    preparation_url = models.CharField(max_length=31, primary_key=True)
    method_name = models.CharField(max_length=63)
    method_description = models.TextField()
    icon = models.ImageField(upload_to="icons", blank=True, null=True)

    def __str__(self):
        return self.method_name


class Storage(models.Model):
    """Model definition for Storage."""

    storage_url = models.CharField(max_length=31, primary_key=True)
    method_name = models.CharField(max_length=63)
    method_description = models.TextField()
    icon = models.ImageField(upload_to="icons", blank=True, null=True)

    def __str__(self):
        return self.method_name
