from django.shortcuts import render

# Create your views here.

def interactive_page(request):
    return render(request, 'interactive_page.html')