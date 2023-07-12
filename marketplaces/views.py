from django.shortcuts import render, get_object_or_404
from .models import Marketplace
from website.models import Announcement
from django.contrib.gis.db.models.functions import Distance
import math

# Create your views here.


def ferias(request):
    """View function for all ferias page of site."""
    
    marketplaces = Marketplace.objects.all().order_by("name")
    total_marketplaces = marketplaces.count()

    n_sanjose = marketplaces.filter(province="San José").count()
    n_alajuela = marketplaces.filter(province="Alajuela").count()
    n_cartago = marketplaces.filter(province="Cartago").count()
    n_heredia = marketplaces.filter(province="Heredia").count()
    n_guanacaste = marketplaces.filter(province="Guanacaste").count()
    n_puntarenas = marketplaces.filter(province="Puntarenas").count()
    n_limon = marketplaces.filter(province="Limón").count()
    n_provinces = [n_sanjose, n_alajuela, n_cartago, n_heredia, n_guanacaste, n_puntarenas, n_limon]

    n_monday = marketplaces.filter(opening_hours__contains="Mo").count()
    n_tuesday = marketplaces.filter(opening_hours__contains="Tu").count()
    n_wednesday = marketplaces.filter(opening_hours__contains="We").count()
    n_thursday = marketplaces.filter(opening_hours__contains="Th").count()
    n_friday = marketplaces.filter(opening_hours__contains="Fr").count()
    n_saturday = marketplaces.filter(opening_hours__contains="Sa").count()
    n_sunday = marketplaces.filter(opening_hours__contains="Su").count()
    n_days = [n_monday, n_tuesday, n_wednesday, n_thursday, n_friday, n_saturday, n_sunday]

    # Find the number of marketplaces where fairground is true
    n_fairground = marketplaces.filter(fairground=True).count() / total_marketplaces * 100
    n_indoor = marketplaces.filter(indoor=True).count() / total_marketplaces * 100
    n_food = marketplaces.filter(food=True).count() / total_marketplaces * 100

    context = {
        "marketplaces": marketplaces,
        "total_marketplaces": total_marketplaces,
        "n_sanjose": n_sanjose,
        "n_alajuela": n_alajuela,
        "n_cartago": n_cartago,
        "n_heredia": n_heredia,
        "n_guanacaste": n_guanacaste,
        "n_puntarenas": n_puntarenas,
        "n_limon": n_limon,
        "n_provinces": n_provinces,
        "n_monday": n_monday,
        "n_tuesday": n_tuesday,
        "n_wednesday": n_wednesday,
        "n_thursday": n_thursday,
        "n_friday": n_friday,
        "n_saturday": n_saturday,
        "n_sunday": n_sunday,
        "n_days": n_days,
        "n_fairground": math.ceil(n_fairground),
        "n_indoor": math.ceil(n_indoor),
        "n_food": math.ceil(n_food),
    }
    return render(request, "ferias.html", context)


def feria(request, marketplace_url):
    """View function for every feria page of site."""

    marketplace = get_object_or_404(Marketplace, pk=marketplace_url)
    closest_marketplaces = (
        Marketplace.objects.annotate(
            distance=Distance("location", marketplace.location)
        )
        .exclude(pk=marketplace_url)
        .order_by("distance")[0:3]
    )
    infrastructure = {
        "campo ferial": marketplace.fairground,
        "espacio bajo techo": marketplace.indoor,
        "servicios sanitarios": marketplace.toilets,
        "lavamanos": marketplace.handwashing,
        "agua potable": marketplace.drinking_water,
        "estacionamiento de bicicletas": marketplace.bicycle_parking,
    }
    services = {
        "comidas": marketplace.food,
        "bebidas": marketplace.drinks,
        "artesanías": marketplace.handicrafts,
        "carnicería": marketplace.butcher,
        "productos lácteos": marketplace.dairy,
        "pescadería": marketplace.seafood,
        "plantas ornamentales": marketplace.garden_centre,
        "floristería": marketplace.florist,
    }
    announcements = Announcement.objects.filter(marketplace=marketplace_url).order_by("-created")
    context = {
        "marketplace": marketplace,
        "closest_marketplaces": closest_marketplaces,
        "infrastructure": infrastructure,
        "services": services,
        "announcements": announcements,
    }

    return render(request, "feria.html", context)
