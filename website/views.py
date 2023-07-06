from django.shortcuts import render
from ferias.forms import MarketplaceForm
from marketplaces.models import Marketplace
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    if request.method == 'POST':
        form = MarketplaceForm(request.POST)
        if form.is_valid():
            # Look for the marketplace in the database
            # Get the answer from the form in the field "fairground"
            fairground = form.cleaned_data['fairground']
            results = Marketplace.objects.filter(fairground=fairground)
            return render(request, 'index.html', {'results': results})
    else:
        form = MarketplaceForm()
    
    context = {
        "marketplace_form": form
    }
    return render(request, 'index.html', context)

def acerca(request):
    return render(request, 'acerca.html')

def contacto(request):
    return render(request, 'contacto.html')