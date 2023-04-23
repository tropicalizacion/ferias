from django.urls import path

from . import views

urlpatterns = [
    path('', views.ferias, name='ferias'),
    path('<str:marketplace_id>/', views.feria, name='feria'),
]