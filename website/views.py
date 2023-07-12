from django.shortcuts import render
from ferias.forms import MarketplaceForm
from marketplaces.models import Marketplace
from .models import Announcement
from django.db.models import Q
from django.contrib.gis.db.models.functions import Distance
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    if request.method == "POST":
        # Search by location
        location = request.POST.get("location")
        print(location)
        if location != "any_location":
            marketplaces = Marketplace.objects.all().order_by("name")
        else:
            if location == "my_location":
                # TODO: Get user location
                coordinates = (9.937087255120892, -84.04391604618372)
            elif location == "some_location":
                # TODO: Get location from input with Nominatim
                coordinates = (9.933364850202214, -84.07706364618377)        
            marketplaces = (
                Marketplace.objects.annotate(
                    distance=Distance("location", coordinates)
                )
                .order_by("distance")[0:5]
            )
        # Search by schedule
        day = request.POST.get("day")
        print(day)
        marketplaces = marketplaces.filter(opening_hours__contains=day)
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
    return render(request, "crear.html")


def anuncio(request, slug):
    announcement = Announcement.objects.get(slug=slug)
    context = {
        "announcement": announcement,
    }
    return render(request, "anuncio.html", context)


def editar(request, slug):
    announcement = Announcement.objects.get(slug=slug)
    context = {
        "announcement": announcement,
    }
    return render(request, "editar.html", context)