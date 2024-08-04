from django.urls import path

from . import views

urlpatterns = [
    path("", views.recipes, name='recetas'),
    path("crear/", views.create_recipe, name='create_recipe'),
    path("<slug:slug>/", views.recipe, name='recipe'),
    path("<slug:slug>/editar", views.edit_recipe, name='edit_recipe'),
    path("<slug:slug>/eliminar", views.delete_recipe, name='delete_recipe'),

    path('<int:i>/crear-ingredientes', views.create_recipe_ingredient_form, name='create_recipe_ingredient_form'),
    path('<int:i>/crear-pasos', views.create_recipe_step_form, name='create_recipe_step_form'),
    path('<int:i>/<slug:slug>/editar-ingredientes', views.edit_recipe_ingredient_form, name='edit_recipe_ingredient_form'),
    path('<int:i>/<slug:slug>/editar-pasos', views.edit_recipe_step_form, name='edit_recipe_step_form'),
]