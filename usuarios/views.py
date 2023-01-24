from django.shortcuts import render

# Create your views here.

def usuarios(request):
    return render(request, 'usuarios.html')

def perfil(request):
    return render(request, 'perfil.html')
