from django.urls import path

from . import views

urlpatterns = [
    path("", views.recipes, name='recetas'),
    path("crear/", views.create_recipe, name='create_recipe'),
    path("<slug:slug>/", views.recipe, name='recipe'),
    path("<slug:slug>/editar", views.edit_recipe, name='edit_recipe'),
    path("<slug:slug>/eliminar", views.delete_recipe, name='delete_recipe'),

    
    path('<int:i>/<slug:slug>/ingredientes', views.recipe_ingredient_form, name='recipe_ingredient_form'),
    path('<int:i>/<slug:slug>/pasos', views.recipe_step_form, name='recipe_step_form'),
]