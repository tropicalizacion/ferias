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

# Create your views here.


def index(request):

    #Obtener la coordenadas de un usuario mediante el IP de su dispositivo
    r = requests.get('https://get.geojs.io/')
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    ipAdd = ip_request.json()['ip']
    url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
    geo_request = requests.get(url)
    geo_data = geo_request.json()

    if request.method == "POST":
        # Search by location
        location = request.POST.get("location")
        print(location)

        if location == "any_location": #All marketplaces
            marketplaces = Marketplace.objects.all().order_by("name")
        elif location == "my_location": # Search marketplace by user location
            #Get longitude
            locationLon = float(request.POST.get("longitudeValue"))
            print(locationLon)
            print(type(locationLon))
            #Get latitude
            locationLat = float(request.POST.get("latitudeValue"))
            print(locationLat)
            print(type(locationLat))
            #Get coordinates
            coordinates = Point(locationLon, locationLat, srid=4326)
            print(coordinates)

            marketplaces = (
                Marketplace.objects.annotate(distance=Distance("location", coordinates)).order_by("distance")
            )

        elif location == "some_location": #Search marketplace by a specific location
            #Get longitude
            locationLonSearch = float(request.POST.get("longitudeValueBusqueda"))
            print(locationLonSearch)
            print(type(locationLonSearch))
            #Get latitude
            locationLatSearch = float(request.POST.get("latitudeValueBusqueda"))
            print(locationLatSearch)
            print(type(locationLatSearch))
            #Get coordinates
            coordinates = Point(locationLonSearch, locationLatSearch, srid=4326)
            print(coordinates)
            marketplaces = (
                Marketplace.objects.annotate(distance=Distance("location", coordinates)).order_by("distance")
            )
        else:
            print("No hay ferias disponibles")
            
        # Search by schedule
        '''
        day = request.POST.get("day")
        print(day)
        marketplaces = marketplaces.filter(opening_hours__contains=day)
        '''
        # Search by amenities
        query = Q() 
        fairground = request.POST.get("fairground")
        if fairground is not None:
            query &= Q(fairground=fairground)
        indoor = request.POST.get("indoor")
        if indoor is not None:
            query &= Q(indoor=indoor)
        marketplaces = marketplaces.filter(query)
        context = {
            "marketplaces": marketplaces,
        }
        return render(request, "index.html", context)
    else:
        return render(request, "index.html")


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
