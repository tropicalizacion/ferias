from django.urls import path

from . import views

urlpatterns = [
    path('', views.products, name='productos'),
    path('precios/', views.prices, name='precios'),
    path('<str:product_url>/', views.product),
    path('api/prices-data/', views.prices_data, name='prices_data'),
]