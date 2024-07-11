from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import RecipeForm, RecipeIngredientFormSet, StepFormSet
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
    recipe_form = RecipeForm()
    ingredient_formset = RecipeIngredientFormSet(prefix='ingredients')
    step_formset = StepFormSet(prefix='steps')

    # Aquí el usuario ya envió el formulario con los datos. Se revisa que sea válido el form y se guarda en la BD.
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES) # FILES nos permite guardar una imagen.
        ingredient_formset = RecipeIngredientFormSet(request.POST, prefix='ingredients') # Este es el nombre del conjunto de formularios de ingredientes.
        step_formset = StepFormSet(request.POST, request.FILES, prefix='steps') # Este es el nombre del conjunto de formularios de pasos.

        if recipe_form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            recipe = recipe_form.save()
            ingredient_formset.instance = recipe # Esto vincula los ingredientes a instance (la receta que se acaba de crear).
            ingredient_formset.save()
            step_formset.instance = recipe # Esto vincula los pasos a esa misma receta creada.
            step_formset.save()
            return render(request, "create_recipe.html") # Aquí se debería redireccionar a la página principal de recetas.
            # return render(request, "recipe.html", slug=recipe.slug)
    
    # Si es un GET, envía al template los formularios vacíos.
    context = {
        'recipe_form': recipe_form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'ingredients': Ingredient.objects.all(),
    }
    return render(request, "create_recipe.html", context)


# Este view hace lo mismo que create_recipe, pero en lugar de enviar los formularios vacíos en GET, primero obtiene los datos de la receta de la BD.
def edit_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    recipe_form = RecipeForm(instance=recipe)
    ingredient_formset = RecipeIngredientFormSet(instance=recipe, prefix='ingredients')
    step_formset = StepFormSet(instance=recipe, prefix='steps')

    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = RecipeIngredientFormSet(request.POST, instance=recipe, prefix='ingredients')
        step_formset = StepFormSet(request.POST, request.FILES, instance=recipe, prefix='steps')

        if recipe_form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            recipe = recipe_form.save()
            ingredient_formset.save()
            step_formset.save()
            return render(request, "create_recipe.html") # Aquí se debería redireccionar a la página principal de recetas.
            # return render(request, "recipe.html", slug=recipe.slug) 

    context = {
        'recipe_form': recipe_form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'ingredients': Ingredient.objects.all(),
    }
    return render(request, "create_recipe.html", context)


"""
def create_recipe(request):
    if (request.method == 'POST'):
        form = RecipeForm(request.POST)
        if (form.is_valid()):
            recipe_name = form.cleaned_data['name']
            recipe = Recipe.objects.create(name=recipe_name)
            recipe.save()
            return HttpResponse(f'Recipe was created with name {recipe.name}')
    form = CreateRecipeForm()
    return render(request, "create_recipe.html", {'form': form})


def edit_recipe(request, slug):
    return render(request, "create_recipe.html")
"""
