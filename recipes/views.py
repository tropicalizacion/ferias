from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest
from .forms import RecipeForm, RecipeIngredientFormSet, StepFormSet, IngredientForm
from .models import Ingredient, Category, Tag, Recipe, RecipeIngredient, Step

# Create your views here.


# TODO: Mostrar un mensaje de receta creada.
# TODO: Mostrar un mensaje de receta eliminada.
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


@login_required
def create_recipe(request):
    recipe_form = RecipeForm()
    ingredient_formset = RecipeIngredientFormSet(prefix="ingredients")
    step_formset = StepFormSet(prefix="steps")

    if request.method == "POST":
        recipe_form = RecipeForm(request.POST, request.FILES) 
        ingredient_formset = RecipeIngredientFormSet(request.POST, prefix="ingredients")
        step_formset = StepFormSet(request.POST, request.FILES, prefix="steps")

        if recipe_form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            recipe = recipe_form.save()
            recipe.user = request.user
            recipe.save()
            ingredient_formset.save()
            step_formset.save()

            return redirect("recipe", recipe_id=recipe.id)
        
        else:
            print(recipe_form.errors)
            print(ingredient_formset.errors)
            print(step_formset.errors)

    context = {
        "title": "Crear receta",
        "recipe_form": recipe_form,
        "ingredient_formset": ingredient_formset,
        "step_formset": step_formset,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
        "ingredients": Ingredient.objects.all(),
    }
    
    return render(request, 'create_recipe.html', context)


# Este view hace lo mismo que create_recipe, pero en lugar de enviar los formularios vacíos en GET, primero obtiene los datos de la receta de la BD.
@login_required
def edit_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    recipe_form = RecipeForm(instance=recipe)
    ingredient_formset = RecipeIngredientFormSet(instance=recipe, prefix="ingredients")
    step_formset = StepFormSet(instance=recipe, prefix="steps")

    if request.method == "POST":
        recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = RecipeIngredientFormSet(request.POST, instance=recipe, prefix="ingredients")
        step_formset = StepFormSet(request.POST, request.FILES, instance=recipe, prefix="steps")

        if recipe_form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            recipe = recipe_form.save()
            recipe.user = request.user
            recipe.save()
            ingredient_formset.save()
            step_formset.save()

            return redirect("recipe", slug=recipe.slug)
        else:
            print(recipe_form.errors)
            print(ingredient_formset.errors)
            print(step_formset.errors)

    context = {
        "title": "Editar receta",
        "recipe": recipe,
        "recipe_form": recipe_form,
        "ingredient_formset": ingredient_formset,
        "step_formset": step_formset,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
        "ingredients": Ingredient.objects.all(),
    }
    
    return render(request, 'create_recipe.html', context)




@login_required
def delete_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)

    # Verifica si el usuario tiene el los permisos necesarios
    if request.user.is_staff:
        recipe.delete()
        messages.success(request, "Se eliminó la receta.")
    else:
        messages.error(request, "No tiene permisos para eliminar esta receta.")

    return redirect("recetas")


@login_required
def recipe_ingredient_form(request, i:int, slug=None):
    recipe = get_object_or_404(Recipe, slug=slug)
    ingredient_formset = RecipeIngredientFormSet(instance=recipe)
    ingredient_formset.min_num = i

    context = {
        "next_ingredient": i + 1,
        "recipe": recipe,
        "form": ingredient_formset.forms[i],
        "management_form": ingredient_formset.management_form
    }

    return render(request, "partials/recipe_ingredient_form.html", context)


@login_required
def recipe_step_form(request, i:int, slug=None):
    recipe = get_object_or_404(Recipe, slug=slug)
    step_formset = StepFormSet(instance=recipe)
    step_formset.min_num = i

    context = {
        "next_step": i + 1,
        "recipe": recipe,
        "form": step_formset.forms[i],
        "management_form": step_formset.management_form
    }

    return render(request, "partials/recipe_step_form.html", context)

