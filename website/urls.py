from django.urls import path
from .views import index
from .views import acerca
from . import views

urlpatterns = [
    path('', views.cover, name='cover'),
    path('index', views.index, name='index'), 
    path('acerca/', views.acerca, name='acerca'),
    path('contacto/', views.contacto, name='contacto'),
    
]