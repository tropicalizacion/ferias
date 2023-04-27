from django.db import models

# Create your models here.


class Product(models.Model):
    """Model definition for Product."""
    CATEGORY_CHOICES = [
        (1, 'Legumbres'),
        (2, 'Tubérculos'),
        (3, 'Raíces'),
        (4, 'Cereales'),
        (5, 'Frutas'),
        (6, 'Especies'),
        (7, 'Hortalizas'),
        (8, 'No convencionales'),
    ]
    SEASON_CHOICES = [
        (0, 'Sin disponibilidad'),
        (1, 'Poca disponibilidad'),
        (2, 'Buena disponibilidad'),
        (3, 'Temporada alta'),
    ]
    CENTER_ORIGIN_CHOICES = [
        (1, '(I) Asia Oriental'),
        (2, '(II) Subcontinente indio'),
        (3, '(IIa) Archipiélago indo-malayo'),
        (4, '(III) Asia Central'),
        (5, '(IV) Asia Menor y Creciente Fértil'),
        (6, '(V) Mediterráneo'),
        (7, '(VI) Abisinia (actual Etiopía)'),
        (8, '(VII) Mesoamérica'),
        (9, '(VIII) Región andina tropical'),
        (10, '(VIIIa) Región chilena'),
        (11, '(VIIIb) Región brasileña-paraguaya'),
        (12, 'Sin clasificación'),
    ]

    product_id = models.AutoField(primary_key=True)
    product_url = models.CharField(max_length=63, blank=False, null=False)
    category = models.PositiveIntegerField(
        choices=CATEGORY_CHOICES, blank=False, null=False)
    scientific_name = models.CharField(max_length=63, blank=False, null=False)
    scientific_name_variety = models.CharField(
        max_length=63, blank=True, null=True)
    common_name = models.CharField(max_length=63, blank=False, null=False)
    common_name_variety = models.CharField(
        max_length=63, blank=True, null=True)
    common_name_variety_alternate = models.CharField(
        max_length=63, blank=True, null=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    icon = models.ImageField(upload_to='icons', blank=True, null=True)
    center_origin = models.IntegerField(
        choices=CENTER_ORIGIN_CHOICES, blank=True, null=True)
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
    nutrition_comment = models.TextField(blank=True, null=True)
    preparation = models.ManyToManyField('Preparation', blank=True)
    storage = models.ManyToManyField('Storage', blank=True)

    def __str__(self):
        return self.common_name


class Preparation(models.Model):
    """Model definition for Preparation."""

    preparation_url = models.CharField(max_length=31, primary_key=True)
    method_name = models.CharField(max_length=63)
    method_description = models.TextField()

    def __str__(self):
        return self.method_name


class Storage(models.Model):
    """Model definition for Storage."""

    storage_url = models.CharField(max_length=31, primary_key=True)
    method_name = models.CharField(max_length=63)
    method_description = models.TextField()

    def __str__(self):
        return self.method_name
