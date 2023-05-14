from django.db import models

# Create your models here.


class Product(models.Model):
    """Model definition for Product."""

    CATEGORY_CHOICES = [
        ("verdura", "Verdura (hortaliza)"),
        ("legumbre", "Legumbre (leguminosa)"),
        ("tubérculo", "Tubérculo (raíz)"),
        ("grano", "Grano (cereal)"),
        ("fruta", "Fruta"),
        ("fruto seco", "Fruto seco (nuez)"),
        ("condimento", "Condimento (especia)"),
        ("no convencional", "No convencional"),
    ]
    CENTER_ORIGIN_CHOICES = [
        ("I", "Asia Oriental"),
        ("II", "Subcontinente indio"),
        ("IIa", "Archipiélago indo-malayo"),
        ("III", "Asia Central"),
        ("IV", "Asia Menor y Creciente Fértil"),
        ("V", "Mediterráneo"),
        ("VI", "Abisinia (actual Etiopía)"),
        ("VII", "Mesoamérica"),
        ("VIII", "Región andina tropical"),
        ("VIIIa", "Región chilena"),
        ("VIIIb", "Región brasileña-paraguaya"),
        ("N/A", "Sin clasificación"),
    ]
    # "From Vavilov to the Present: A Review" C. Earle Smith, Jr., Economic Botany, Vol. 23, No. 1 (Jan. - Mar., 1969), pp. 2-19 (18 pages)

    product_url = models.CharField(
        primary_key=True, max_length=63, blank=False, null=False
    )
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=15)
    common_name = models.CharField(max_length=63, blank=False, null=False)
    common_name_alternate = models.CharField(max_length=127, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to="icons", blank=True, null=True)
    center_origin = models.CharField(
        choices=CENTER_ORIGIN_CHOICES, max_length=5, blank=True, null=True
    )
    food_basket = models.BooleanField(default=False)
    nutrition_notes = models.TextField(blank=True, null=True)
    preparation = models.ManyToManyField("Preparation", blank=True)
    preparation_notes = models.TextField(blank=True, null=True)
    storage = models.ManyToManyField("Storage", blank=True)
    storage_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.common_name


class Variety(models.Model):
    """Model definition for Variety."""

    SEASON_CHOICES = [
        (0, "Sin disponibilidad"),
        (1, "Poca disponibilidad"),
        (2, "Buena disponibilidad"),
        (3, "Temporada alta"),
    ]

    variety_id = models.AutoField(primary_key=True)
    product_url = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True)
    scientific_name = models.CharField(max_length=63, blank=False, null=False)
    scientific_name_variety = models.CharField(max_length=63, blank=True, null=True)
    common_name_variety = models.CharField(
        max_length=63, blank=True, null=True, default=""
    )
    common_name_variety_alternate = models.CharField(
        max_length=127, blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="products", blank=True, null=True)
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

    def __str__(self):
        return f"({self.product_url}) {self.common_name_variety}"


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
