# Generated by Django 5.0.6 on 2024-10-10 23:24

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("products", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=63)),
            ],
        ),
        migrations.CreateModel(
            name="Marketplace",
            fields=[
                (
                    "marketplace_url",
                    models.CharField(
                        help_text="URL utilizada para la feria",
                        max_length=50,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(help_text="Nombre de la feria", max_length=127),
                ),
                (
                    "name_alternate",
                    models.CharField(
                        blank=True,
                        help_text="Nombre alternativo de la feria",
                        max_length=127,
                        null=True,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="Descripción de la feria", null=True
                    ),
                ),
                (
                    "opening_hours",
                    models.CharField(
                        blank=True,
                        help_text="Horario de apertura de la feria, con el formato de la especificación de OpenStreetMap para opening_hours",
                        max_length=1023,
                        null=True,
                    ),
                ),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(
                        blank=True,
                        help_text="Ubicación exacta de la feria",
                        null=True,
                        srid=4326,
                    ),
                ),
                (
                    "area",
                    django.contrib.gis.db.models.fields.PolygonField(
                        blank=True,
                        help_text="Área en que la feria está ubicada",
                        null=True,
                        srid=4326,
                    ),
                ),
                (
                    "size",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("S", "Pequeña"),
                            ("M", "Mediana"),
                            ("L", "Grande"),
                            ("XL", "Muy grande"),
                        ],
                        help_text="Tamaño de la feria, puede ser una de las cuatro opciones: S, M, L o XL",
                        max_length=2,
                        null=True,
                    ),
                ),
                (
                    "province",
                    models.CharField(
                        help_text="Provincia en que se encuentra la feria",
                        max_length=31,
                    ),
                ),
                (
                    "canton",
                    models.CharField(
                        help_text="Cantón en que se encuentra la feria", max_length=31
                    ),
                ),
                (
                    "district",
                    models.CharField(
                        help_text="Distrito en que se encuentra la feria", max_length=31
                    ),
                ),
                (
                    "postal_code",
                    models.IntegerField(
                        blank=True, help_text="Código postal de la feria", null=True
                    ),
                ),
                (
                    "address",
                    models.TextField(
                        blank=True, help_text="Dirección exacta de la feria", null=True
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        help_text="Número telefónico de contacto de la feria",
                        max_length=127,
                        null=True,
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        help_text="Correo electrónico de la feria",
                        max_length=127,
                        null=True,
                    ),
                ),
                (
                    "website",
                    models.URLField(
                        blank=True,
                        help_text="Sitio web de la feria",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "facebook",
                    models.URLField(
                        blank=True,
                        help_text="Página de Facebook de la feria",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "instagram",
                    models.URLField(
                        blank=True,
                        help_text="Perfil de Instagram de la feria",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "opening_date",
                    models.DateField(
                        blank=True, help_text="Fecha de apertura de la feria", null=True
                    ),
                ),
                (
                    "operator",
                    models.CharField(
                        blank=True,
                        help_text="Operador u organizador de la feria",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "branch",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Atlántico", "Comité Regional Atlántico"),
                            ("Brunca", "Comité Regional Brunca"),
                            ("Central Central", "Comité Regional Central Central"),
                            (
                                "Central Occidental Este",
                                "Comité Regional Central Occidental Este",
                            ),
                            (
                                "Central Occidental Oeste",
                                "Comité Regional Central Occidental Oeste",
                            ),
                            ("Central Oriental", "Comité Regional Central Oriental"),
                            ("Chorotega", "Comité Regional Chorotega"),
                            ("Huetar Norte", "Comité Regional Huetar Norte"),
                            ("Pacífico Central", "Comité Regional Pacífico Central"),
                        ],
                        help_text="Comité regional al que pertenece la feria",
                        max_length=63,
                        null=True,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("feria", "Feria del Agricultor"),
                            ("mercado", "Mercado Libre"),
                            ("otro", "Otro tipo de feria"),
                        ],
                        help_text="Tipo de feria, puede ser uno de los tres tipos: feria, mercado u otro",
                        max_length=31,
                        null=True,
                    ),
                ),
                (
                    "parking",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("lane", "en la calle"),
                            ("street_side", "al lado de la calle en espacio dedicado"),
                            ("surface", "un un espacio amplio de parqueo"),
                        ],
                        help_text="Tipo de parqueo disponible en la feria, puede ser uno de los tres tipos: lane, street_side o surface",
                        max_length=31,
                        null=True,
                    ),
                ),
                (
                    "bicycle_parking",
                    models.BooleanField(
                        blank=True,
                        help_text="Parqueo para bicicletas disponible en la feria",
                        null=True,
                    ),
                ),
                (
                    "fairground",
                    models.BooleanField(
                        blank=True,
                        help_text="Plaza ferial disponible para la feria",
                        null=True,
                    ),
                ),
                (
                    "indoor",
                    models.BooleanField(
                        blank=True,
                        help_text="Espacio techado disponible en la feria",
                        null=True,
                    ),
                ),
                (
                    "toilets",
                    models.BooleanField(
                        blank=True, help_text="Baños disponibles en la feria", null=True
                    ),
                ),
                (
                    "handwashing",
                    models.BooleanField(
                        blank=True,
                        help_text="Lavamanos disponibles en la feria",
                        null=True,
                    ),
                ),
                (
                    "drinking_water",
                    models.BooleanField(
                        blank=True,
                        help_text="Agua potable disponible en la feria",
                        null=True,
                    ),
                ),
                (
                    "food",
                    models.BooleanField(
                        blank=True,
                        help_text="Venta de alimentos en la feria",
                        null=True,
                    ),
                ),
                (
                    "drinks",
                    models.BooleanField(
                        blank=True, help_text="Venta de bebidas en la feria", null=True
                    ),
                ),
                (
                    "handicrafts",
                    models.BooleanField(
                        blank=True,
                        help_text="Venta de artesanías en la feria",
                        null=True,
                    ),
                ),
                (
                    "butcher",
                    models.BooleanField(
                        blank=True, help_text="Venta de carnes en la feria", null=True
                    ),
                ),
                (
                    "dairy",
                    models.BooleanField(
                        blank=True, help_text="Venta de lácteos en la feria", null=True
                    ),
                ),
                (
                    "seafood",
                    models.BooleanField(
                        blank=True, help_text="Venta de mariscos en la feria", null=True
                    ),
                ),
                (
                    "spices",
                    models.BooleanField(
                        blank=True, help_text="Venta de especias en la feria", null=True
                    ),
                ),
                (
                    "garden_centre",
                    models.BooleanField(
                        blank=True, help_text="Venta de plantas en la feria", null=True
                    ),
                ),
                (
                    "florist",
                    models.BooleanField(
                        blank=True, help_text="Venta de flores en la feria", null=True
                    ),
                ),
                (
                    "other_services",
                    models.CharField(
                        blank=True,
                        help_text="Otros servicios disponibles en la feria",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "varieties",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Variedades de productos disponibles en la feria",
                        to="products.variety",
                    ),
                ),
                (
                    "payment",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Métodos de pago aceptados en la feria",
                        to="marketplaces.payment",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MarketplaceHistory",
            fields=[
                (
                    "marketplace_history_id",
                    models.CharField(max_length=127, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=127)),
                (
                    "name_alternate",
                    models.CharField(blank=True, max_length=127, null=True),
                ),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "opening_hours",
                    models.CharField(blank=True, max_length=1023, null=True),
                ),
                ("opening_date", models.DateField(blank=True, null=True)),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(
                        blank=True, null=True, srid=4326
                    ),
                ),
                (
                    "area",
                    django.contrib.gis.db.models.fields.PolygonField(
                        blank=True, null=True, srid=4326
                    ),
                ),
                ("province", models.CharField(max_length=31)),
                ("canton", models.CharField(max_length=31)),
                ("district", models.CharField(max_length=31)),
                ("postal_code", models.IntegerField(blank=True, null=True)),
                ("address", models.TextField(blank=True, null=True)),
                (
                    "size",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("S", "Pequeña"),
                            ("M", "Mediana"),
                            ("L", "Grande"),
                            ("XL", "Muy grande"),
                        ],
                        max_length=2,
                        null=True,
                    ),
                ),
                ("phone", models.IntegerField(blank=True, null=True)),
                ("email", models.EmailField(blank=True, max_length=127, null=True)),
                ("website", models.URLField(blank=True, max_length=127, null=True)),
                ("instagram", models.URLField(blank=True, max_length=127, null=True)),
                ("facebook", models.URLField(blank=True, max_length=127, null=True)),
                ("operator", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "branch",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Atlántico", "Comité Regional Atlántico"),
                            ("Brunca", "Comité Regional Brunca"),
                            ("Central Central", "Comité Regional Central Central"),
                            (
                                "Central Occidental Este",
                                "Comité Regional Central Occidental Este",
                            ),
                            (
                                "Central Occidental Oeste",
                                "Comité Regional Central Occidental Oeste",
                            ),
                            ("Central Oriental", "Comité Regional Central Oriental"),
                            ("Chorotega", "Comité Regional Chorotega"),
                            ("Huetar Norte", "Comité Regional Huetar Norte"),
                            ("Pacífico Central", "Comité Regional Pacífico Central"),
                        ],
                        max_length=63,
                        null=True,
                    ),
                ),
                (
                    "parking",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("lane", "en la calle"),
                            ("street_side", "al lado de la calle en espacio dedicado"),
                            ("surface", "un un espacio amplio de parqueo"),
                        ],
                        max_length=31,
                        null=True,
                    ),
                ),
                ("bicycle_parking", models.BooleanField(blank=True, null=True)),
                ("fairground", models.BooleanField(blank=True, null=True)),
                ("indoor", models.BooleanField(blank=True, null=True)),
                ("toilets", models.BooleanField(blank=True, null=True)),
                ("handwashing", models.BooleanField(blank=True, null=True)),
                ("drinking_water", models.BooleanField(blank=True, null=True)),
                ("food", models.BooleanField(blank=True, null=True)),
                ("drinks", models.BooleanField(blank=True, null=True)),
                ("handicrafts", models.BooleanField(blank=True, null=True)),
                ("butcher", models.BooleanField(blank=True, null=True)),
                ("dairy", models.BooleanField(blank=True, null=True)),
                ("seafood", models.BooleanField(blank=True, null=True)),
                ("garden_centre", models.BooleanField(blank=True, null=True)),
                ("florist", models.BooleanField(blank=True, null=True)),
                (
                    "other_services",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("saved_at", models.DateTimeField(auto_now_add=True)),
                ("comments_reviewer", models.TextField(blank=True, null=True)),
                (
                    "marketplace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="marketplaces.marketplace",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "varieties",
                    models.ManyToManyField(blank=True, to="products.variety"),
                ),
                (
                    "payment",
                    models.ManyToManyField(blank=True, to="marketplaces.payment"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Photo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="marketplaces")),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        help_text="Descripción de la foto (alt).",
                        max_length=255,
                        null=True,
                    ),
                ),
                ("alt", models.CharField(blank=True, max_length=255, null=True)),
                ("profile", models.BooleanField(blank=True, default=False, null=True)),
                ("cover", models.BooleanField(blank=True, default=False, null=True)),
                (
                    "marketplace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="marketplaces.marketplace",
                    ),
                ),
            ],
        ),
    ]
