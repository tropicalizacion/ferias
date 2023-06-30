from django.urls import path

from . import views

urlpatterns = [
    path('', views.advice, name='consejos'),
    path('preparacion/', views.preparations, name='preparacion'),
    path('preparacion/<str:preparation_url>/', views.preparation),
    path('almacenamiento/', views.storages, name='almacenamiento'),
    path('almacenamiento/<str:storage_url>/', views.storage),
    path('visitar/', views.visit, name='visitar'),
    path('paradas/', views.stops, name='paradas'),
]