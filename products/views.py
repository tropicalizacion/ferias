from django.shortcuts import render, get_object_or_404
from .models import Product, Variety, Price
from website.models import Text
import datetime

# Create your views here.


def products(request):
    """View function for all products page of site."""
    month = datetime.datetime.now().month
    varieties = Variety.objects.all().order_by("product_url")
    varieties_otros = varieties.filter(product_url__category="otro")
    varieties_frutas = varieties.filter(product_url__category="fruta")
    varieties_hierbas = varieties.filter(product_url__category="hierba")
    varieties_verduras = varieties.filter(product_url__category="verdura")
    varieties_legumbres = varieties.filter(product_url__category="legumbre")
    varieties_tuberculos = varieties.filter(product_url__category="tubérculo")
    
    text = Text.objects.filter(page="/productos")
    texts = {}
    texts["hero"] = text.filter(section="hero").first()
    texts["hero_parentesis"] = text.filter(section="hero_parentesis").first()
    texts["lista"] = text.filter(section="lista").first()
    texts["lista_descripcion"] = text.filter(section="lista_descripcion").first()
    
    context = {
        "month": month,
        "varieties_otros": varieties_otros,
        "varieties_frutas": varieties_frutas,
        "varieties_hierbas": varieties_hierbas,
        "varieties_verduras": varieties_verduras,
        "varieties_legumbres": varieties_legumbres,
        "varieties_tuberculos": varieties_tuberculos,
        "texts": texts
    }
    return render(request, "products.html", context)


def product(request, product_url):
    """View function for product page of site."""

    product = get_object_or_404(Product, product_url=product_url)
    varieties = Variety.objects.filter(product_url=product_url)
    context = {
        "product": product,
        "varieties": varieties,
    }

    return render(request, "product.html", context)


def prices(request):
    prices = Price.objects.all()
    year = datetime.datetime.now().isocalendar()[0]
    week = datetime.datetime.now().isocalendar()[1]
    week_prices = prices.filter(year=year, week=week)

    context = {
        "prices": prices,
        "week_prices": week_prices,
    }
    return render(request, "prices.html", context)