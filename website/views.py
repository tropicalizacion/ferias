from django.shortcuts import render, redirect
from marketplaces.models import Marketplace
from .models import Announcement
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from marketplaces.views import search_marketplaces
from django.contrib.auth import login, authenticate, logout


def cover(request):
    return render(request, "cover.html")


def index(request):
    if request.method == "POST":
        marketplaces_match, marketplaces_others, marketplaces_keyword, keyword, query_text = search_marketplaces(request.POST)
        context = {
            "show_results": True,
            "query_text": query_text,
            "keyword": keyword,
            "marketplaces_match": marketplaces_match,
            "marketplaces_others": marketplaces_others,
            "marketplaces_keyword": marketplaces_keyword,
        }
        return render(request, "index.html", context)
    else:
        return render(request, "index.html")


def acerca(request):
    return render(request, "acerca.html")


def ingresar(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html", {"error": True})
    else:
        if request.user.is_authenticated:
            context = {"logged_in": True}
        else:
            context = {"logged_in": False}
        return render(request, "login.html", context)


def salir(request):
    logout(request)
    url = "/ingresar/?logout=true"
    return redirect(url)


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
