from django.shortcuts import render
from ferias.forms import MarketplaceForm
from marketplaces.models import Marketplace
from django.http import HttpResponseRedirect
from django.db.models import Q

# Create your views here.


def index(request):
    if request.method == "POST":
        query = Q()
        
        fairground = request.POST.get("fairground")
        if fairground is not None:
            query &= Q(fairground=fairground)
        indoor = request.POST.get("indoor")
        if indoor is not None:
            query &= Q(indoor=indoor)
        results = Marketplace.objects.filter(query).order_by('name')
        context = {
            'results': results,
            'query': query,
        }
        return render(request, "index.html", context)
    else:
        return render(request, "index.html")


def acerca(request):
    return render(request, "acerca.html")


def contacto(request):
    return render(request, "contacto.html")
