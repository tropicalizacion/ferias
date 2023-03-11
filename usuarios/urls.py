from django.urls import path
from . import views
from .views import registro,login_usuario,logout_usuario

#URLs de las páginas de usuarios
urlpatterns = [
    path('', views.usuarios, name='usuarios'),
    path('perfil/', views.perfil, name='perfil'),
    path('registro/', views.registro, name='registro'),
    path('login_usuario/', views.login_usuario, name='login_usuario'),
    path('logout_usuario/', views.logout_usuario, name='logout_usuario'),
]