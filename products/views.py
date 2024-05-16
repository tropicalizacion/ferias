from django.shortcuts import render, get_object_or_404
from .models import Product, Variety
from website.models import Text
import datetime
import jsonpickle

# JSON-LD Structured Data

def get_structured_data(product):
    structured_data = {
        "@context": "http://schema.org/",
        "@type": "MenuItem",
        "additionalType": "Produce",
        "name": product.common_name,
        "alternateName": product.common_name_alternate,
        "description": product.description,
        "image": "", # product.icon.url,
        "nutrition": {
            "@type": "NutritionInformation",
            "name": product.category,
            "description": product.nutrition_notes
        },
        "menuAddOn": {
            "@type": "MenuSection",
            "additionalType": "Storage",
            "description": product.storage_notes
            # "countryOfOrigin": parse_country_origin(product.center_origin),
        }
    }

    return structured_data

def parse_country_origin(key):
    regions_mapping = {
        'I': 'Asia Oriental',
        'II': 'Subcontinente indio',
        'IIa': 'Archipiélago indo-malayo',
        'III': 'Asia Central',
        'IV': 'Asia Menor y Creciente Fértil',
        'V': 'Mediterráneo',
        'VI': 'Abisinia (actual Etiopía)',
        'VII': 'Mesoamérica',
        'VIII': 'Región andina tropical',
        'VIIIa': 'Región chilena',
        'VIIIb': 'Región brasileña-paraguaya'
    }

    return regions_mapping[key]

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

    structured_data = get_structured_data(product)
    serialized_json = jsonpickle.encode(structured_data, unpicklable=False)
    structured_data = jsonpickle.decode(serialized_json)

    context = {
        "product": product,
        "varieties": varieties,
        "structured_data": structured_data
    }

    return render(request, "product.html", context)
