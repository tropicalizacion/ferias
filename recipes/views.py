from django.shortcuts import render, get_object_or_404
from .models import Ingredient, Category, Tag, Recipe, RecipeIngredient, Step

# Create your views here.


def recipes(request):
    recipes = Recipe.objects.all()
    context = {"recipes": recipes}
    return render(request, "recipes.html", context)


def recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    recipe_steps = Step.objects.filter(recipe=recipe)
    context = {
        "recipe": recipe,
        "recipe_ingredients": recipe_ingredients,
        "recipe_steps": recipe_steps,
    }
    return render(request, "recipe.html", context)


def create_recipe(request):
    return render(request, "create_recipe.html")


def edit_recipe(request, slug):
    return render(request, "create_recipe.html")
