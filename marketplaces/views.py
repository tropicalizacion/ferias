from django.shortcuts import render, get_object_or_404
from .models import Marketplace

# Create your views here.


def ferias(request):
    """View function for all ferias page of site."""
    return render(request, 'ferias.html')


def feria(request, marketplace_id):
    """View function for every feria page of site."""

    marketplace = get_object_or_404(Marketplace, pk=marketplace_id)
    context = {
        'marketplace': marketplace,
    }
    
    return render(request, 'feria.html', context)
