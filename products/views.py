from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.


def products(request):
    """View function for all products page of site."""
    return render(request, "products.html")


def product(request, product_url):
    """View function for product page of site."""

    product = get_object_or_404(Product, product_url=product_url)
    context = {"product": product}

    return render(request, "product.html", context)
