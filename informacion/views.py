from django.shortcuts import render

# Create your views here.

def interactivo(request):
    return render(request, 'interactivo.html')