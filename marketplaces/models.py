from django.contrib.gis.db import models
from products.models import Variety
from django.contrib.auth.models import User

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
        ("lane", "en la calle"),
        ("street_side", "al lado de la calle en espacio dedicado"),
        ("surface", "un un espacio amplio de parqueo"),
    ]
    MARKETPLACE_TYPE_CHOICES = [
        ("feria", "Feria del Agricultor"),
        ("mercado", "Mercado Libre"),
        ("otro", "Otro tipo de feria"),
    ]

    marketplace_url = models.CharField(
        max_length=50, primary_key=True, help_text="URL utilizada para la feria"
    )
    # General information
    name = models.CharField(max_length=127, help_text="Nombre de la feria")
    name_alternate = models.CharField(
        max_length=127,
        blank=True,
        null=True,
        help_text="Nombre alternativo de la feria",
    )
    description = models.TextField(
        blank=True, null=True, help_text="Descripción de la feria"
    )
    opening_hours = models.CharField(
        max_length=1023,
        blank=True,
        null=True,
        help_text="Horario de apertura de la feria, con el formato de la especificación de OpenStreetMap para opening_hours",
    )
    location = models.PointField(
        blank=True, null=True, help_text="Ubicación exacta de la feria"
    )
    area = models.PolygonField(
        blank=True, null=True, help_text="Área en que la feria está ubicada"
    )
    size = models.CharField(
        choices=SIZE_CHOICES,
        max_length=2,
        blank=True,
        null=True,
        help_text="Tamaño de la feria, puede ser una de las cuatro opciones: S, M, L o XL",
    )
    province = models.CharField(
        max_length=31, help_text="Provincia en que se encuentra la feria"
    )
    canton = models.CharField(
        max_length=31, help_text="Cantón en que se encuentra la feria"
    )
    district = models.CharField(
        max_length=31, help_text="Distrito en que se encuentra la feria"
    )
    postal_code = models.IntegerField(
        blank=True, null=True, help_text="Código postal de la feria"
    )
    address = models.TextField(
        blank=True, null=True, help_text="Dirección exacta de la feria"
    )
    phone = models.IntegerField(
        blank=True, null=True, help_text="Número telefónico de contacto de la feria"
    )
    email = models.EmailField(
        max_length=127,
        blank=True,
        null=True,
        help_text="Correo electrónico de la feria",
    )
    website = models.URLField(
        max_length=255, blank=True, null=True, help_text="Sitio web de la feria"
    )
    facebook = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Página de Facebook de la feria",
    )
    instagram = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Perfil de Instagram de la feria",
    )
    opening_date = models.DateField(
        blank=True, null=True, help_text="Fecha de apertura de la feria"
    )
    operator = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Operador u organizador de la feria",
    )
    branch = models.CharField(
        choices=BRANCH_CHOICES,
        max_length=63,
        blank=True,
        null=True,
        help_text="Comité regional al que pertenece la feria",
    )
    marketplace_type = models.CharField(
        max_length=31,
        choices=MARKETPLACE_TYPE_CHOICES,
        blank=True,
        null=True,
        help_text="Tipo de feria, puede ser uno de los tres tipos: feria, mercado u otro",
    )
    # Infrastructure
    parking = models.CharField(
        choices=PARKING_CHOICES,
        max_length=31,
        blank=True,
        null=True,
        help_text="Tipo de parqueo disponible en la feria, puede ser uno de los tres tipos: lane, street_side o surface",
    )
    bicycle_parking = models.BooleanField(
        blank=True,
        null=True,
        help_text="Parqueo para bicicletas disponible en la feria",
    )
    fairground = models.BooleanField(
        blank=True, null=True, help_text="Plaza ferial disponible para la feria"
    )
    indoor = models.BooleanField(
        blank=True, null=True, help_text="Espacio techado disponible en la feria"
    )
    toilets = models.BooleanField(
        blank=True, null=True, help_text="Baños disponibles en la feria"
    )
    handwashing = models.BooleanField(
        blank=True, null=True, help_text="Lavamanos disponibles en la feria"
    )
    drinking_water = models.BooleanField(
        blank=True, null=True, help_text="Agua potable disponible en la feria"
    )
    # Services
    food = models.BooleanField(
        blank=True, null=True, help_text="Venta de alimentos en la feria"
    )
    drinks = models.BooleanField(
        blank=True, null=True, help_text="Venta de bebidas en la feria"
    )
    handicrafts = models.BooleanField(
        blank=True, null=True, help_text="Venta de artesanías en la feria"
    )
    butcher = models.BooleanField(
        blank=True, null=True, help_text="Venta de carnes en la feria"
    )
    dairy = models.BooleanField(
        blank=True, null=True, help_text="Venta de lácteos en la feria"
    )
    seafood = models.BooleanField(
        blank=True, null=True, help_text="Venta de mariscos en la feria"
    )
    spices = models.BooleanField(
        blank=True, null=True, help_text="Venta de especias en la feria"
    )
    garden_centre = models.BooleanField(
        blank=True, null=True, help_text="Venta de plantas en la feria"
    )
    florist = models.BooleanField(
        blank=True, null=True, help_text="Venta de flores en la feria"
    )
    # Other
    payment = models.ManyToManyField(
        "Payment", blank=True, help_text="Métodos de pago aceptados en la feria"
    )
    other_services = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Otros servicios disponibles en la feria",
    )
    # Products (varieties)
    varieties = models.ManyToManyField(
        Variety, blank=True, help_text="Variedades de productos disponibles en la feria"
    )

    def __str__(self):
        return self.name


class Photo(models.Model):
    """Model definition for Photo."""

    marketplace = models.ForeignKey(Marketplace, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="marketplaces")
    description = models.CharField(
        max_length=255, blank=True, null=True, help_text="Descripción de la foto (alt)."
    )
    alt = models.CharField(max_length=255, blank=True, null=True)
    profile = models.BooleanField(default=False, blank=True, null=True)
    cover = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.url


class Payment(models.Model):
    """Model definition for Payment."""

    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class MarketplaceHistory(models.Model):
    """Model definition for Marketplace (la feria) historical records."""

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
        ("surface", "un un espacio amplio de parqueo"),
    ]

    marketplace_history_id = models.CharField(max_length=127, primary_key=True)
    marketplace = models.ForeignKey("Marketplace", on_delete=models.CASCADE)
    # General information
    name = models.CharField(max_length=127)
    name_alternate = models.CharField(max_length=127, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    opening_hours = models.CharField(max_length=1023, blank=True, null=True)
    opening_date = models.DateField(blank=True, null=True)
    location = models.PointField(blank=True, null=True)
    area = models.PolygonField(blank=True, null=True)
    province = models.CharField(max_length=31)
    canton = models.CharField(max_length=31)
    district = models.CharField(max_length=31)
    postal_code = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    size = models.CharField(choices=SIZE_CHOICES, max_length=2, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=127, blank=True, null=True)
    website = models.URLField(max_length=127, blank=True, null=True)
    instagram = models.URLField(max_length=127, blank=True, null=True)
    facebook = models.URLField(max_length=127, blank=True, null=True)
    operator = models.CharField(max_length=255, blank=True, null=True)
    branch = models.CharField(
        choices=BRANCH_CHOICES, max_length=63, blank=True, null=True
    )
    # Infrastructure
    parking = models.CharField(
        choices=PARKING_CHOICES, max_length=31, blank=True, null=True
    )
    bicycle_parking = models.BooleanField(blank=True, null=True)
    fairground = models.BooleanField(blank=True, null=True)
    indoor = models.BooleanField(blank=True, null=True)
    toilets = models.BooleanField(blank=True, null=True)
    handwashing = models.BooleanField(blank=True, null=True)
    drinking_water = models.BooleanField(blank=True, null=True)
    # Services
    food = models.BooleanField(blank=True, null=True)
    drinks = models.BooleanField(blank=True, null=True)
    handicrafts = models.BooleanField(blank=True, null=True)
    butcher = models.BooleanField(blank=True, null=True)
    dairy = models.BooleanField(blank=True, null=True)
    seafood = models.BooleanField(blank=True, null=True)
    garden_centre = models.BooleanField(blank=True, null=True)
    florist = models.BooleanField(blank=True, null=True)
    # Other
    payment = models.ManyToManyField("Payment", blank=True)
    other_services = models.CharField(max_length=255, blank=True, null=True)
    # Products (varieties)
    varieties = models.ManyToManyField(Variety, blank=True)
    # History
    saved_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comments_reviewer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.saved_at})"
