from django.shortcuts import render

# Create your views here.

def ferias(request):
    return render(request, 'ferias.html')
