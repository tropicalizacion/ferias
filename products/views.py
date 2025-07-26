from django.shortcuts import render, get_object_or_404
from .models import Product, Variety, Price
from website.models import Text
import datetime
from .models import Price, Variety
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from datetime import timedelta
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
        "texts": texts,
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
    varieties = (
        Variety.objects.filter(has_price=True)
        .select_related("product_url")
        .all()
    )
    prices = Price.objects.all()

    today = datetime.date.today()
    one_year_ago = today - timedelta(days=365)
    
    this_week_prices = prices.filter(publication_date__gte=one_year_ago)

    context = {
        "prices": prices,
        "this_week_prices": this_week_prices,
        "varieties": varieties,
    }
    return render(request, "prices.html", context)

@require_GET
def prices_data(request):
    ids = request.GET.get('ids', '')
    range_type = request.GET.get('range', '')  # nuevo parámetro, e.g. 'last_year'

    variety_ids = [i for i in ids.split(',') if i]
    qs = (
        Price.objects
        .filter(variety__variety_id__in=variety_ids)
        .order_by('publication_date')
        .select_related('variety__product_url')
    )

    if range_type == 'last_year':
        one_year_ago = datetime.date.today() - timedelta(days=365)
        qs = qs.filter(publication_date__gte=one_year_ago)

    data = {}
    for p in qs:
        vid = p.variety.variety_id
        label = p.variety.product_url.common_name
        if p.variety.common_name_variety:
            label += f' {p.variety.common_name_variety}'
        if vid not in data:
            data[vid] = {'label': label, 'data': []}
        data[vid]['data'].append({
            'x': p.publication_date.isoformat(),
            'y': p.price
        })

    series = list(data.values())
    return JsonResponse({'series': series})