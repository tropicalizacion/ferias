from django.shortcuts import render, get_object_or_404
from .models import Marketplace
from website.models import Announcement
from django.contrib.gis.db.models.functions import Distance
import osm_opening_hours_humanized as ooh
import math
import json

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

    n_fairground = marketplaces.filter(fairground=True).count() / total_marketplaces * 100
    n_indoor = marketplaces.filter(indoor=True).count() / total_marketplaces * 100
    n_parking = marketplaces.filter(parking="surface").count() / total_marketplaces * 100
    n_infrastructure = [n_fairground, n_indoor, n_parking]

    n_food = marketplaces.filter(food=True).count() / total_marketplaces * 100
    n_drinks = marketplaces.filter(drinks=True).count() / total_marketplaces * 100
    n_handicrafts = marketplaces.filter(handicrafts=True).count() / total_marketplaces * 100
    n_butcher = marketplaces.filter(butcher=True).count() / total_marketplaces * 100
    n_dairy = marketplaces.filter(dairy=True).count() / total_marketplaces * 100
    n_seafood = marketplaces.filter(seafood=True).count() / total_marketplaces * 100
    n_garden_centre = marketplaces.filter(garden_centre=True).count() / total_marketplaces * 100
    n_florist = marketplaces.filter(florist=True).count() / total_marketplaces * 100
    n_amenities = [n_food, n_drinks, n_handicrafts, n_butcher, n_dairy, n_seafood, n_garden_centre, n_florist]
    n_amenities = [math.ceil(i) for i in n_amenities]

    marketplaces_map = []
    for marketplace in marketplaces:
        marketplace_dict = {}
        marketplace_dict["name"] = marketplace.name
        marketplace_dict["latitude"] = marketplace.location.y
        marketplace_dict["longitude"] = marketplace.location.x
        marketplaces_map.append(marketplace_dict)
    
    marketplaces_map = json.dumps(marketplaces_map)

    context = {
        "marketplaces": marketplaces,
        "marketplaces_map": marketplaces_map,
        "total_marketplaces": total_marketplaces,
        "n_provinces": n_provinces,
        "n_days": n_days,
        "n_infrastructure": n_infrastructure,
        "n_amenities": n_amenities,
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
    #horarios
    opening_hours = marketplace.opening_hours
    horarios_separados = opening_hours.split(";")
    horarios_humanizados = []
# Crea una instancia del analizador de opening_hours
    for horario in horarios_separados:
     parser = ooh.OHParser(horario.strip(), locale="es")
# Obtiene la descripción humanizada del horario
     horario_texto = "".join(parser.description())
     horario_texto = horario_texto.replace("On ", "")
     horarios_humanizados.append(horario_texto)
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
	"horarios_humanizados": horarios_humanizados,
        "announcements": announcements,
    }

    return render(request, "feria.html", context)
