from django.shortcuts import render
from ferias.forms import MarketplaceForm
from marketplaces.models import Marketplace
from django.db.models import Q
from django.contrib.gis.db.models.functions import Distance
import requests
from django.contrib.gis.geos import Point


def index(request):

    # Search by amenities
    amenities = {"parking": 'parqueo', "bicycle_parking": 'parqueo para bicicletas', "fairground": 'campo ferial', "indoor": 'bajo techo', "toilets": 'servicios sanitarios', "handwashing": 'lavado de manos', "drinking_water": 'agua potable', "food": 'comidas', 'drinks': 'bebidas', "handicrafts": 'artesanías', "butcher": 'carnicería', "dairy": 'productos lácteos', "seafood": 'pescadería y mariscos', "garden_centre": 'plantas', "florist": 'floristería'}

    if request.method == "POST":
        # Search by location
        location = request.POST.get("location")

            #All marketplaces
        if location == "any_location":
            marketplaces = Marketplace.objects.all().order_by("name")

            # Search marketplace by user location
        elif location == "my_location":

            longitude = float(request.POST.get("longitudeValue"))
            latitude = float(request.POST.get("latitudeValue"))
            coordinates = Point(longitude, latitude, srid=4326)

            marketplaces = (
                Marketplace.objects.annotate(distance=Distance("location", coordinates)).order_by("distance")
            )

            #Search marketplace by a specific location
        elif location == "some_location":

            longitude = float(request.POST.get("longitudeValueBusqueda"))
            latitude = float(request.POST.get("latitudeValueBusqueda"))
            coordinates = Point(longitude, latitude, srid=4326)

            marketplaces = (
                Marketplace.objects.annotate(distance=Distance("location", coordinates)).order_by("distance")
            )
        else:
            print("No hay ferias disponibles")
            
        # Search by schedule
        day = request.POST.get("day")
        if day != "NA":
            marketplaces = marketplaces.filter(opening_hours__contains=day)
    
        query = Q() 
        for key, value in amenities.items():
            key = request.POST.get(key)
            if key is not None:
                key = str(key)
                query &= Q(key=True)
            marketplaces = marketplaces.filter(query)

        context = {
            "marketplaces": marketplaces,
            "amenities" : amenities
        }
        return render(request, "index.html", context)
    else:
        context = {
            "amenities" : amenities
        }
        return render(request, "index.html",context)


def acerca(request):
    return render(request, "acerca.html")


def contacto(request):
    return render(request, "contacto.html")
