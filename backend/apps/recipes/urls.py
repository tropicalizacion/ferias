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

    path('<int:i>/eliminar-ingrediente', views.delete_recipe_ingredient_form, name='delete_recipe_ingredient_form'),
    path('<int:i>/eliminar-paso', views.delete_recipe_step_form, name='delete_recipe_step_form'),
    path('<int:i>/<slug:slug>/eliminar-ingrediente-existente', views.delete_existing_recipe_ingredient_form, name='delete_existing_recipe_ingredient_form'),
    path('<int:i>/<slug:slug>/eliminar-paso-existente', views.delete_existing_recipe_step_form, name='delete_existing_recipe_step_form'),

    path('crear-categoria', views.create_category, name='create_category'),
    path('crear-etiqueta', views.create_tag, name='create_tag'),
    path('crear-ingrediente', views.create_ingredient, name='create_ingredient'),
]