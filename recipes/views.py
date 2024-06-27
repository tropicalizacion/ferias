from django.shortcuts import render

from .models import Ingredient, Category, Tag, Recipe, RecipeIngredient, Step

# Create your views here.


def recipes(request):
    return render(request, "recipes.html")


def recipe(request, slug):
    return render(request, "recipe.html")


def create_recipe(request):
    return render(request, "create_recipe.html")


def edit_recipe(request, slug):
    return render(request, "create_recipe.html")
