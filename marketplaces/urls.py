from django.urls import path

from . import views

urlpatterns = [
    path("", views.ferias, name="ferias"),
    path("buscar/", views.results, name="results"),
    path("<str:marketplace_url>/", views.feria, name="feria"),
    path("<str:marketplace_url>/editar/", views.edit, name="edit"),
]
