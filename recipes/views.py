from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from .models import Ingredient, Category, Tag, Recipe, RecipeIngredient, Step
from .forms import RecipeForm, RecipeIngredientFormSet, StepFormSet, IngredientForm, CategoryForm, TagForm
from datetime import timedelta


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

    # JSON-LD Structured Data
    initial_data = get_structured_data(recipe, recipe_steps)
    structured_data = json.loads(json.dumps(initial_data))

    context = {
        "recipe": recipe,
        "recipe_ingredients": recipe_ingredients,
        "recipe_steps": recipe_steps,
        "structured_data": structured_data,
    }
    return render(request, "recipe.html", context)


# @login_required
def create_recipe(request):
    recipe_form = RecipeForm()
    ingredient_formset = RecipeIngredientFormSet(prefix="ingredients")
    step_formset = StepFormSet(prefix="steps")
    ingredient_form = IngredientForm()
    category_form = CategoryForm()
    tag_form = TagForm()

    if request.method == "POST":
        recipe_form = RecipeForm(request.POST, request.FILES)

        if recipe_form.is_valid():
            recipe = recipe_form.save()
            recipe.save()

            ingredient_formset = RecipeIngredientFormSet(request.POST, instance=recipe, prefix="ingredients")
            step_formset = StepFormSet(request.POST, request.FILES, instance=recipe, prefix="steps")

            ingredient_formset = save_recipe_ingredients(ingredient_formset)
            step_formset = save_recipe_steps(step_formset)

            if ingredient_formset.is_valid() and step_formset.is_valid():
                return redirect("recipe", slug=recipe.slug)

    next_ingredient = 0 if len(ingredient_formset.forms) is None else len(ingredient_formset.forms)
    next_step = 0 if len(step_formset.forms) is None else len(step_formset.forms)

    context = {
        "title": "Crear receta",
        "recipe_form": recipe_form,
        "ingredient_formset": ingredient_formset,
        "next_ingredient": next_ingredient,
        "step_formset": step_formset,
        "next_step": next_step,
        "ingredient_form": ingredient_form,
        "category_form": category_form,
        "tag_form": tag_form,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
        "ingredients": Ingredient.objects.all(),
    }
    
    return render(request, "create_recipe.html", context)


# Este view hace lo mismo que create_recipe, pero en lugar de enviar los formularios vacíos en GET, primero obtiene los datos de la receta de la BD.
# @login_required
def edit_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    recipe_form = RecipeForm(instance=recipe)
    ingredient_formset = RecipeIngredientFormSet(instance=recipe, prefix="ingredients")
    step_formset = StepFormSet(instance=recipe, prefix="steps")
    ingredient_form = IngredientForm()
    category_form = CategoryForm()
    tag_form = TagForm()
    
    if request.method == "POST":
        recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)

        if recipe_form.is_valid():
            recipe = recipe_form.save()
            recipe.save()

            ingredient_formset = RecipeIngredientFormSet(request.POST, instance=recipe, prefix="ingredients")
            step_formset = StepFormSet(request.POST, request.FILES, instance=recipe, prefix="steps")

            ingredient_formset = save_recipe_ingredients(ingredient_formset)
            step_formset = save_recipe_steps(step_formset)

            if ingredient_formset.is_valid() and step_formset.is_valid():
                return redirect("recipe", slug=recipe.slug)

    next_ingredient = 0 if len(ingredient_formset.forms) is None else len(ingredient_formset.forms)
    next_step = 0 if len(step_formset.forms) is None else len(step_formset.forms)

    context = {
        "title": "Editar receta",
        "recipe": recipe,
        "recipe_form": recipe_form,
        "ingredient_formset": ingredient_formset,
        "next_ingredient": next_ingredient,
        "step_formset": step_formset,
        "next_step": next_step,
        "ingredient_form": ingredient_form,
        "category_form": category_form,
        "tag_form": tag_form,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
        "ingredients": Ingredient.objects.all(),
    }
    
    return render(request, 'create_recipe.html', context)


# @login_required
def delete_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)

    if recipe:
        recipe.delete()
        messages.success(request, "Se eliminó la receta.")
    else:
        messages.error(request, "Error al eliminar la receta.")

    return redirect("recetas")


# @login_required
def create_recipe_ingredient_form(request, i: int):
    ingredient_formset = RecipeIngredientFormSet(prefix="ingredients")
    ingredient_formset.min_num = i + 1

    context = {
        "current_ingredient": i,
        "next_ingredient": i + 1,
        "recipe": recipe,
        "form": ingredient_formset.forms[i],
        "management_form": ingredient_formset.management_form
    }

    return render(request, "partials/recipe_ingredient_form.html", context)


# @login_required
def edit_recipe_ingredient_form(request, i:int, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    ingredient_formset = RecipeIngredientFormSet(instance=recipe, prefix="ingredients")
    ingredient_formset.min_num = i + 1

    context = {
        "current_ingredient": i,
        "next_ingredient": i + 1,
        "recipe": recipe,
        "form": ingredient_formset.forms[i],
        "management_form": ingredient_formset.management_form
    }

    return render(request, "partials/recipe_ingredient_form.html", context)


def delete_recipe_ingredient_form(request, i: int):
    ingredient_formset = RecipeIngredientFormSet(prefix="ingredients")

    if i <= len(ingredient_formset.forms):
        ingredient_formset.forms.pop(i)

    context = {
        "current_ingredient": i - 1,
        "next_ingredient": i,
        "recipe": recipe,
        "form": None,
        "management_form": ingredient_formset.management_form
    }

    return render(request, "partials/recipe_ingredient_form.html", context)


def delete_existing_recipe_ingredient_form(request, i: int, slug):   
    recipe = get_object_or_404(Recipe, slug=slug)
    ingredient_formset = RecipeIngredientFormSet(instance=recipe, prefix="ingredients")
    
    if i <= len(ingredient_formset.forms):
        ingredient_formset.forms.pop(i)
    
    context = {
        "current_ingredient": i - 1,
        "next_ingredient": i - 1,
        "recipe": recipe,
        "form": None,
        "management_form": ingredient_formset.management_form
    }

    return render(request, "partials/recipe_ingredient_form.html", context)


# @login_required
def create_recipe_step_form(request, i:int):
    step_formset = StepFormSet(prefix="steps")
    step_formset.min_num = i + 1

    context = {
        "next_step": i + 1,
        "recipe": recipe,
        "form": step_formset.forms[i],
        "management_form": step_formset.management_form
    }

    return render(request, "partials/recipe_step_form.html", context)


# @login_required
def edit_recipe_step_form(request, i:int, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    step_formset = StepFormSet(instance=recipe, prefix="steps")
    step_formset.min_num = i + 1

    context = {
        "next_step": i + 1,
        "recipe": recipe,
        "form": step_formset.forms[i],
        "management_form": step_formset.management_form
    }

    return render(request, "partials/recipe_step_form.html", context)


def delete_recipe_step_form(request, i: int):
    step_formset = StepFormSet(prefix="steps")
    
    if i <= len(step_formset.forms):
        step_formset.forms.pop(i)
        
    context = {
        "current_step": i - 1,
        "next_step": i,
        "recipe": recipe,
        "form": None,
        "management_form": step_formset.management_form
    }

    return render(request, "partials/recipe_step_form.html", context)


def delete_existing_recipe_step_form(request, i: int, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    step_formset = StepFormSet(instance=recipe, prefix="steps")
    
    if i <= len(step_formset.forms):
        step_formset.forms.pop(i)
    
    context = {
        "current_step": i - 1,
        "next_step": i - 1,
        "recipe": recipe,
        "form": None,
        "management_form": step_formset.management_form
    }

    return render(request, "partials/recipe_step_form.html", context)


def save_recipe_ingredients(formset):
    for form in formset:
        if form.is_valid():
            recipe_ingredient = form.save(commit=False)

            existing_ingredient = RecipeIngredient.objects.filter(
                recipe=recipe_ingredient.recipe,
                ingredient=recipe_ingredient.ingredient
            ).first()

            if existing_ingredient:
                existing_ingredient.unit = recipe_ingredient.unit
                existing_ingredient.quantity = recipe_ingredient.quantity
                existing_ingredient.save()
            else:
                recipe_ingredient.save()

    return formset


def save_recipe_steps(formset):
    for form in formset:
        if form.is_valid():
            recipe_step = form.save(commit=False)

            existing_step = Step.objects.filter(
                recipe=recipe_step.recipe, 
                step_sequence=recipe_step.step_sequence
            ).first()

            if existing_step:
                existing_step.title = recipe_step.title
                existing_step.description = recipe_step.description
                existing_step.photo = recipe_step.photo
                existing_step.save()
            else:
                recipe_step.save()

    return formset


def create_ingredient(request):
    form = IngredientForm()

    if request.method == 'POST' and request.htmx:
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.save()
            
            form.cleaned_data['allergies'] 
            ingredient.allergies.set(form.cleaned_data['allergies'])
    
    context = {
        "ingredient_form": form,
        "ingredients": Ingredient.objects.all()
    }

    return render(request, 'partials/new_ingredient.html', context)


def create_category(request):
    recipe = RecipeForm()

    if request.method == 'POST' and request.htmx:
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            category.save()

    context = {
        "recipe_form": recipe,
        "categories": Category.objects.all(),
    }

    return render(request, 'partials/category_list.html', context)


def create_tag(request):
    recipe = RecipeForm()

    if request.method == 'POST' and request.htmx:
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            tag.save()

    context = {
        "recipe_form": recipe,
        "tags": Tag.objects.all(),
    }
    
    return render(request, 'partials/tag_list.html', context)


def get_structured_data(recipe, recipe_steps):
    structured_data = {
        "@context": "http://schema.org/",
        "@type": "Recipe",
        "name": recipe.name,
        "description": recipe.description,
        "image": recipe.image.url if recipe.image else None,
        "prepTime": format_duration(recipe.prep_time) if recipe.prep_time else None,
        "cookTime": format_duration(recipe.cook_time) if recipe.cook_time else None,
        "totalTime": format_duration(recipe.total_time) if recipe.total_time else None,
        "recipeYield": recipe.recipe_yield,
        "recipeIngredient": [ingredient.ingredient.ingredient_name for ingredient in recipe.recipeingredient_set.all()],
        "recipeInstructions": [step.to_dict() for step in recipe_steps],
        "recipeCategory": recipe.category.category_name if recipe.category else None,
        "recipeCuisine": recipe.recipe_cuisine if recipe.recipe_cuisine else None,
        "keywords": list(recipe.tags.values_list('tag_name', flat=True)),
        "nutrition": {
            "@type": "NutritionInformation",
            "calories": recipe.calories if recipe.calories else "No disponible",
            "fatContent": recipe.fat_content if recipe.fat_content else "No disponible",
            "carbohydrateContent": recipe.carbohydrate_content if recipe.carbohydrate_content else "No disponible",
            "proteinContent": recipe.protein_content if recipe.protein_content else "No disponible",
        }
    }

    return structured_data


def format_duration(duration):
    if isinstance(duration, timedelta):
        total_seconds = int(duration.total_seconds())
    else:
        raise ValueError("Expected a timedelta object")

    total_seconds = total_seconds * 60
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f"PT{hours}H{minutes}M{seconds}S"