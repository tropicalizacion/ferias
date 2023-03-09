from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate

# Create your views here.

def usuarios(request):
    return render(request, 'usuarios.html')

def perfil(request):
    return render(request, 'perfil.html')

def registro(request):
    if request.method == 'POST':
        primer_nombre = request.POST['primer_nombre']
        primer_apellido = request.POST['primer_apellido']
        username = request.POST['username']
        correo = request.POST['correo']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Una cuenta asociada a este correo ya existe')
                return redirect(registro)
            else:
                user: User.objects.create_user(username=username, password=password, email=correo, primer_nombre=primer_nombre, primer_apellido=primer_apellido)
                user.set_password(password)
                user.save()
                print("success")
                return redirect('login_usuario')
    else:
        return render(request, 'registro.html')
    
def login_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Usuario o contraseña incorrectas')
            return redirect('login_usuario')
    else:
        return render(request, 'login.html')
    
def logout_usuario(request):
    auth.logout(request)
    return redirect('index')
