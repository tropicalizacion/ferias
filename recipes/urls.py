from django.urls import path

from . import views

urlpatterns = [
    path("", views.recipes, name="recipes"),
    path("crear/", views.create_recipe, name="create_recipe"),
    path("<slug:slug>/", views.recipe, name="recipe"),
    path("<slug:slug>/editar", views.edit_recipe, name="edit_recipe"),
]
