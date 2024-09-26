from django.contrib.gis.db import models

# Create your models here.


class Product(models.Model):
    """Model definition for Product."""

    CATEGORY_CHOICES = [
        ("verdura", "Verdura u hortaliza"),
        ("fruta", "Fruta"),
        ("cereal", "Cereal o grano"),
        ("legumbre", "Legumbre o leguminosa"),
        ("raiz", "Tubérculo o raíz"),
        ("condimento", "Condimento o especia"),
        ("hierba", "Hierba aromática"),
        ("otro", "Otra categoría"),
    ]

    product_url = models.CharField(primary_key=True, max_length=63)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=15)
    common_name = models.CharField(max_length=63)
    common_name_alternate = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to="images/icons", blank=True, null=True)
    name_origin = models.TextField(blank=True, null=True)
    center_origin = models.ManyToManyField("Origin", blank=True)
    center_origin_notes = models.TextField(blank=True, null=True)
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

    variety_id = models.CharField(max_length=127, primary_key=True)
    product_url = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    scientific_name = models.CharField(max_length=63, blank=False, null=False)
    scientific_name_variety = models.CharField(max_length=63, blank=True, null=True)
    common_name_variety = models.CharField(max_length=63, blank=True, null=True)
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
        string = self.product_url.common_name
        if self.common_name_variety:
            string += f" {self.common_name_variety}"
        return string


class Price(models.Model):
    """Model definition for Price."""

    UNIT_CHOICES = [
        ("kg", "Kilogramo"),
        ("u", "Unidad"),
        ("rollo", "Rollo"),
        ("mata", "Mata"),
    ]
    QUALITY_CHOICES = [
        ("primera", "Primera calidad"),
        ("segunda", "Segunda calidad"),
    ]

    price_id = models.AutoField(primary_key=True)
    variety = models.ForeignKey(Variety, on_delete=models.SET_NULL, null=True)
    quality = models.CharField(
        max_length=63, choices=QUALITY_CHOICES, blank=True, null=True
    )
    unit = models.CharField(choices=UNIT_CHOICES, max_length=10)
    price = models.IntegerField()
    publication_date = models.DateField()
    year = models.IntegerField(blank=True, null=True)
    week = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.year = self.publication_date.isocalendar()[0]
        self.week = self.publication_date.isocalendar()[1]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.variety.product_url.common_name} {self.variety.common_name_variety}: {self.publication_date}"


class Origin(models.Model):
    """Model definition for Center of Origin."""

    code = models.CharField(
        primary_key=True,
        max_length=6,
        help_text="Definición según 'From Vavilov to the Present: A Review' C. Earle Smith, Jr., Economic Botany, Vol. 23, No. 1 (Jan. - Mar., 1969), que va desde I hasta VIII.",
    )
    name = models.CharField(max_length=63)
    description = models.TextField(blank=True, null=True)
    region = models.PolygonField(blank=True, null=True)
    mapamundi = models.ImageField(upload_to="maps", blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


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
