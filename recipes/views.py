from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
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
    ingredient_form = IngredientForm()

    # Aquí el usuario ya envió el formulario con los datos. Se revisa que sea válido el form y se guarda en la BD.
    if request.method == "POST":
        recipe_form = RecipeForm(
            request.POST, request.FILES
        )  # FILES nos permite guardar una imagen.
        ingredient_formset = RecipeIngredientFormSet(
            request.POST, prefix="ingredients"
        )  # Este es el nombre del conjunto de formularios de ingredientes.
        step_formset = StepFormSet(
            request.POST, request.FILES, prefix="steps"
        )  # Este es el nombre del conjunto de formularios de pasos.

        if (
            recipe_form.is_valid()
            and ingredient_formset.is_valid()
            and step_formset.is_valid()
        ):
            recipe = recipe_form.save()
            ingredient_formset.instance = recipe  # Esto vincula los ingredientes a instance (la receta que se acaba de crear).
            ingredient_formset.save()
            step_formset.instance = (
                recipe  # Esto vincula los pasos a esa misma receta creada.
            )
            step_formset.save()
            return redirect("recetas")
    else:
        ingredient_formset = RecipeIngredientFormSet(prefix="ingredients")
        step_formset = StepFormSet(prefix="steps")
        return render(
            request,
            "create_recipe.html",
            {
                "title": "Crear receta",
                "recipe_form": recipe_form,
                "ingredient_formset": ingredient_formset,
                "step_formset": step_formset,
                "ingredient_form": ingredient_form,
            },
        )

    # Si es un GET, envía al template los formularios vacíos.
    context = {
        "title": "Crear receta",
        "recipe_form": recipe_form,
        "ingredient_formset": ingredient_formset,
        "step_formset": step_formset,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
        "ingredients": Ingredient.objects.all(),
    }
    return render(request, "create_recipe.html", context)


# Este view hace lo mismo que create_recipe, pero en lugar de enviar los formularios vacíos en GET, primero obtiene los datos de la receta de la BD.
@login_required
def edit_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    recipe_form = RecipeForm(instance=recipe)
    ingredient_formset = RecipeIngredientFormSet(instance=recipe, prefix="ingredients")
    step_formset = StepFormSet(instance=recipe, prefix="steps")

    if request.method == "POST":
        recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = RecipeIngredientFormSet(
            request.POST, instance=recipe, prefix="ingredients"
        )
        step_formset = StepFormSet(
            request.POST, request.FILES, instance=recipe, prefix="steps"
        )

        if (
            recipe_form.is_valid()
            and ingredient_formset.is_valid()
            and step_formset.is_valid()
        ):
            recipe = recipe_form.save()
            ingredient_formset.save()
            step_formset.save()
            return redirect("recetas")
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
    return render(request, "create_recipe.html", context)

@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Verifica si el usuario tiene el los permisos necesarios
    if request.user.is_staff:
        recipe.delete()
        messages.success(request, "Se eliminó la receta.")
    else:
        messages.error(request, "No tiene permisos para eliminar esta receta.")

    return redirect("recetas")


@login_required
def add_ingredient(request):
    if request.method == "POST":
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = IngredientForm()

    return render(request, "create_recipe.html", {"form": form})
