from django.shortcuts import render

# Create your views here.

def api(request):
    return render(request, 'api.html')