from django.urls import path

from . import views

urlpatterns = [
    path('', views.productos, name='productos'),
    path('<str:product_url>/', views.product, name='product'),
]