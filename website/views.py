from django.shortcuts import render, redirect
from ferias.forms import MarketplaceForm
from marketplaces.models import Marketplace
from .models import Announcement
from django.db.models import Q
from django.contrib.gis.db.models.functions import Distance
from django.contrib.auth.decorators import login_required
#from geopy.geocoders import Nominatim
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


def anuncios(request):
    announcements = Announcement.objects.all().order_by("-created")
    context = {
        "announcements": announcements,
    }
    return render(request, "anuncios.html", context)


def crear(request):
    
    marketplaces = Marketplace.objects.all().order_by("name")
    context = {
        "marketplaces": marketplaces,
    }

    if request.method == "POST":
        
        title = request.POST.get("title")
        marketplace = marketplaces.get(marketplace_url=request.POST.get("marketplace"))
        publish = request.POST.get("publish")
        slug = publish + "-" + title.replace(" ", "-").lower()

        announcement = Announcement(
            title=title,
            marketplace=marketplace,
            content=request.POST.get("content"),
            publish=publish,
            until=request.POST.get("until"),
            publisher=request.POST.get("publisher"),
            author=request.user,
            slug=slug,
        )
        announcement.save()
    
    return render(request, "crear.html", context)


def anuncio(request, slug):
    announcement = Announcement.objects.get(slug=slug)
    context = {
        "announcement": announcement,
    }
    return render(request, "anuncio.html", context)


def editar(request, slug):
    if request.method == "POST":
        announcement = Announcement.objects.get(slug=slug)
        announcement.title = request.POST.get("title")
        announcement.marketplace = Marketplace.objects.get(
            marketplace_url=request.POST.get("marketplace")
        )
        announcement.content = request.POST.get("content")
        announcement.publish = request.POST.get("publish")
        announcement.until = request.POST.get("until")
        announcement.publisher = request.POST.get("publisher")
        announcement.save()
        url = "/anuncios/" + announcement.slug + "/"
        return redirect(url)
    else:
        announcement = Announcement.objects.get(slug=slug)
        marketplaces = Marketplace.objects.all().order_by("name")
        context = {
            "announcement": announcement,
            "marketplaces": marketplaces,
        }
        return render(request, "editar.html", context)
