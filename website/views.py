from django.shortcuts import render
from ferias.forms import MarketplaceForm
from marketplaces.models import Marketplace
from django.db.models import Q
from django.contrib.gis.db.models.functions import Distance
#from geopy.geocoders import Nominatim
import requests
from django.contrib.gis.geos import Point

# Create your views here.


def index(request):

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

        if location == "any_location":
            marketplaces = Marketplace.objects.all().order_by("name")
        elif location == "my_location":
            locationLon = float(request.POST.get("longitudeValue"))
            print(locationLon)
            print(type(locationLon))
            locationLat = float(request.POST.get("latitudeValue"))
            print(locationLat)
            print(type(locationLat))
            coordinates = Point(locationLon, locationLat, srid=4326)
            print(coordinates)
            marketplaces = (
                Marketplace.objects.annotate(distance=Distance("location", coordinates)).order_by("distance")
            )
        elif location == "some_location":
            locationLonSearch = float(request.POST.get("longitudeValueBusqueda"))
            print(locationLonSearch)
            print(type(locationLonSearch))
            locationLatSearch = float(request.POST.get("latitudeValueBusqueda"))
            print(locationLatSearch)
            print(type(locationLatSearch))
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
