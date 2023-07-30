from django.shortcuts import render, redirect
from marketplaces.models import Marketplace
from .models import Announcement
from django.db.models import Q
from django.contrib.gis.db.models.functions import Distance
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point


def index(request):

    if request.method == "POST":

        # Search by location

        location = request.POST.get("location")
        if location == "any_location":
            marketplaces = Marketplace.objects.all().order_by("name")
        elif location == "my_location":
            longitude = float(request.POST.get("my_longitude"))
            latitude = float(request.POST.get("my_latitude"))
            coordinates = Point(longitude, latitude, srid=4326)
            marketplaces = Marketplace.objects.annotate(
                distance=Distance("location", coordinates)
            ).order_by("distance")
        elif location == "some_location":
            longitude = float(request.POST.get("some_longitude"))
            latitude = float(request.POST.get("some_latitude"))
            coordinates = Point(longitude, latitude, srid=4326)
            marketplaces = Marketplace.objects.annotate(
                distance=Distance("location", coordinates)
            ).order_by("distance")

        # Search by day of the week

        day = request.POST.get("day")
        if day != "any_day":
            marketplaces = marketplaces.filter(opening_hours__contains=day)

        # Filter results for exact match

        marketplaces_match = marketplaces

        # Filter by size

        size = request.POST.get("size")
        if size != "any_size":
            query_size = Q()
            if "size_s" in request.POST:
                query_size |= Q(size="S")
            if "size_m" in request.POST:
                query_size |= Q(size="M")
            if "size_l" in request.POST:
                query_size |= Q(size="L")
            if "size_xl" in request.POST:
                query_size |= Q(size="XL")
            marketplaces_match = marketplaces_match.filter(query_size)

        # Filter by infrastructure

        query_infrastructure = Q()
        if "fairground" in request.POST:
            query_infrastructure &= Q(fairground=True)
        if "indoor" in request.POST:
            query_infrastructure &= Q(indoor=True)
        if "parking" in request.POST:
            query_infrastructure &= Q(parking="surface")
        marketplaces_match = marketplaces_match.filter(query_infrastructure)

        # Filter by amenities

        query_amenities = Q()
        if "food" in request.POST:
            query_amenities &= Q(food=True)
        if "drinks" in request.POST:
            query_amenities &= Q(drinks=True)
        if "handicrafts" in request.POST:
            query_amenities &= Q(handicrafts=True)
        if "butcher" in request.POST:
            query_amenities &= Q(butcher=True)
        if "dairy" in request.POST:
            query_amenities &= Q(dairy=True)
        if "seafood" in request.POST:
            query_amenities &= Q(seafood=True)
        if "garden_centre" in request.POST:
            query_amenities &= Q(garden_centre=True)
        if "florist" in request.POST:
            query_amenities &= Q(florist=True)
        marketplaces_match = marketplaces_match.filter(query_amenities)

        # Filter by keyword

        marketplaces_keyword = None
        if "keyword" in request.POST:
            keyword = request.POST.get("keyword")
            print(f'Keyword: {keyword}')
            try:
                marketplaces_keyword = marketplaces
                marketplaces_keyword = marketplaces_keyword.filter(
                    Q(name__unaccent__trigram_similar=keyword) | 
                    Q(description__unaccent__trigram_similar=keyword)
                )
            except:
                pass
        
        # Get other marketplaces

        marketplaces_others = marketplaces.difference(marketplaces_match)

        # Query text

        query_text = request.POST.get("query_text")

        context = {
            "query_text": query_text,
            "show_results": True,
            "marketplaces_match": marketplaces_match,
            "marketplaces_others": marketplaces_others,
            "marketplaces_keyword": marketplaces_keyword,
            "keyword": keyword,
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
