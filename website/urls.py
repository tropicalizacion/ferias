from django.urls import path
from .views import index
from .views import acerca
from . import views

urlpatterns = [
    path('', views.index, name='inicio'), 
    path('sobre/', views.acerca, name='sobre'),
    path('sobre/ferias/', views.sobre_ferias, name='sobre-ferias'),
    path('ingresar/', views.ingresar, name='ingresar'),
    path('salir/', views.salir, name='salir'),
    path('contacto/', views.contacto, name='contacto'),
    path('anuncios/', views.anuncios, name='anuncios'),
    path('anuncios/crear/', views.crear, name='crear_anuncio'),
    path('anuncios/<slug:slug>/', views.anuncio, name='anuncio'),
    path('anuncios/<slug:slug>/editar', views.editar, name='anuncio'),
    path('404', views.custom_404, name='404')
]