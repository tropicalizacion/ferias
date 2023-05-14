from django.shortcuts import render, get_object_or_404
from .models import Marketplace
from django.contrib.gis.db.models.functions import Distance

# Create your views here.


def ferias(request):
    """View function for all ferias page of site."""
    marketplaces = Marketplace.objects.all()
    context = {"marketplaces": marketplaces}
    return render(request, "ferias.html", context)


def feria(request, marketplace_url):
    """View function for every feria page of site."""

    marketplace = get_object_or_404(Marketplace, pk=marketplace_url)
    closest_marketplaces = (
        Marketplace.objects.annotate(
            distance=Distance("location", marketplace.location)
        )
        .exclude(pk=marketplace_url)
        .order_by("distance")[0:3]
    )
    context = {
        "marketplace": marketplace,
        "closest_marketplaces": closest_marketplaces,
    }

    return render(request, "feria.html", context)
