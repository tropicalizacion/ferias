from django.urls import path

from . import views

urlpatterns = [
    path('', views.interactive_page, name='interactivo'),
]