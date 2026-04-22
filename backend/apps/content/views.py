from django.shortcuts import render, get_object_or_404
from products.models import Preparation, Storage

# Create your views here.


def advice(request):
    return render(request, "advice.html")


def preparations(request):
    """View function for preparations page of site."""
    preparations = Preparation.objects.all()
    context = {"preparations": preparations}
    return render(request, "preparations.html", context)


def preparation(request, preparation_url):
    """View function for preparation page of site."""
    preparation = get_object_or_404(Preparation, preparation_url=preparation_url)
    context = {"preparation": preparation}
    return render(request, "preparation.html", context)


def storages(request):
    """View function for storages page of site."""
    storages = Storage.objects.all()
    context = {"storages": storages}
    return render(request, "storages.html", context)


def storage(request, storage_url):
    """View function for storage page of site."""
    storage = get_object_or_404(Storage, storage_url=storage_url)
    context = {"storage": storage}
    return render(request, "storage.html", context)


def visit(request):
    return render(request, "visit.html")


def stops(request):
    return render(request, "stops.html")