from django.shortcuts import render, get_object_or_404
from .models import Marketplace
from django.contrib.gis.db.models.functions import Distance

# Create your views here.


def ferias(request):
    """View function for all ferias page of site."""
    marketplaces = Marketplace.objects.all().order_by("name")
    context = {"marketplaces": marketplaces}
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
    context = {
        "marketplace": marketplace,
        "closest_marketplaces": closest_marketplaces,
        "infrastructure": infrastructure,
        "services": services,
    }

    return render(request, "feria.html", context)
