from django.urls import path
from .views import index
from .views import acerca
from . import views

urlpatterns = [
    path('', views.cover, name='cover'),
    path('index', views.index, name='index'), 
    path('acerca/', views.acerca, name='acerca'),
    path('contacto/', views.contacto, name='contacto'),
    path('anuncios/', views.anuncios, name='anuncios'),
    path('anuncios/crear/', views.crear, name='crear_anuncio'),
    path('anuncios/<slug:slug>/', views.anuncio, name='anuncio'),
    path('anuncios/<slug:slug>/editar', views.editar, name='anuncio'),
]