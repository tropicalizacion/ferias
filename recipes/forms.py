from django import forms
from django.utils.text import slugify
from .models import Recipe, RecipeIngredient, Step, Tag, Ingredient, Category, Tag, Variety, Allergy


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].empty_label = "Seleccione una categoría..."
        self.fields["image"].required = False

    class Meta:
        model = Recipe 
        fields = [
            "id",
            "name",
            "description",
            "category",
            "image",
            "tags",
            "cook_time",
            "prep_time",
            "total_time",
            "recipe_yield",
            "recipe_cuisine",
            "calories",
            "fat_content",
            "carbohydrate_content",
            "protein_content",
        ]
        widgets = {
            "id": forms.HiddenInput(),
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "tags": forms.CheckboxSelectMultiple(attrs={"class": "form-check-inline"}),
            "cook_time": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "hh:mm:ss"}
            ),
            "prep_time": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "hh:mm:ss"}
            ),
            "total_time": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "hh:mm:ss"}
            ),
            "recipe_yield": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "recipe_cuisine": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "ej., Costarricense"}
            ),
            "calories": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "fat_content": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "carbohydrate_content": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "protein_content": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
        }


class RecipeIngredientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ingredient"].empty_label = "Seleccione un ingrediente..."
        self.fields["unit"].choices = RecipeIngredient.UNIT_CHOICES

        self.fields["ingredient"].required = False
        self.fields["unit"].required = False
        self.fields["quantity"].required = False

    class Meta:
        model = RecipeIngredient
        fields = ["id", "ingredient", "unit", "quantity"]
        widgets = {
            "id": forms.HiddenInput(),
            "ingredient": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "unit": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Cantidad",
                    "min": 0,
                    "step": 0.25
                }
            ),
        }


# Cada receta va a tener varias instancias de RecipeIngredientForm.
# forms.inlineformset_factory() permite crear un conjunto de formularios (formset) relacionados a un modelo padre por medio de foreign keys.
RecipeIngredientFormSet = forms.inlineformset_factory(
    Recipe,  # Modelo padre.
    RecipeIngredient,  # Modelo hijo.
    form=RecipeIngredientForm,  # Formulario a desplegar.
    extra=0,  # Mostrar un formulario extra inicialmente.
)


class StepForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["step_sequence"].widget.attrs.update(
            {"min": 1}
        )  # Debe tener al menos un paso.

    class Meta:
        model = Step
        fields = [
            "id",
            "step_sequence",
            "title",
            "description",
            "photo",
        ]
        widgets = {
            "id": forms.HiddenInput(),
            "step_sequence": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Número",
                    "min": 1,
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Título",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descripción",
                    "rows": 1,
                }
            ),
            "photo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "type": "file",
                }
            ),
        }


# Cada receta va a tener varias instancias de StepForm.
StepFormSet = forms.inlineformset_factory(
    Recipe,  # Modelo padre.
    Step,  # Modelo hijo.
    form=StepForm,  # Formulario a desplegar.
    extra=0,  # Mostrar un formulario extra inicialmente.
)


class IngredientForm(forms.ModelForm):
    allergies = forms.MultipleChoiceField(
        choices=[(key, value) for key, value in Allergy.ALLERGY_CHOICES.items()],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="allergies"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ingredient_product"].empty_label = "Seleccione un producto..."
        self.fields["ingredient_name"].widget.attrs.update({
            "placeholder": "Nombre",
        })

        self.fields["ingredient_name"].required = False
        self.fields["ingredient_description"].required = False
        self.fields["ingredient_product"].required = False

    class Meta:
        model = Ingredient
        fields = [
            "ingredient_name",
            "ingredient_description",
            "ingredient_product",
            "allergies",
        ]
        widgets = {
            "ingredient_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "ingredient_description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Descripción",
                }
            ),
            "ingredient_product": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category_name"].widget.attrs.update({
            "placeholder": "Nombre",
        })

        self.fields["category_name"].required = False
        self.fields["category_description"].required = False
        self.fields["category_slug"].required = False

    class Meta:
        model = Category
        fields = ['category_name', 'category_description', 'category_slug']

        widgets = {
            "category_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre",
                }
            ),
            "category_description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Descripción",
                }
            ),
            "category_slug": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Slug"
                }
            )
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('category_slug')
        if not slug:
            name = self.cleaned_data.get('category_name')
            if name:
                slug = slugify(name)
        return slug

    def clean_name(self):
        name = self.cleaned_data.get('category_name')
        if Category.objects.filter(category_name=name).exists():
            raise forms.ValidationError("Esta categoría ya existe.")
        return name


class TagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tag_name"].widget.attrs.update({
            "placeholder": "Nombre",
        })

        self.fields["tag_name"].required = False
        self.fields["tag_slug"].required = False

    class Meta:
        model = Tag
        fields = ['tag_name', 'tag_slug']

        widgets = {
            "tag_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre",
                }
            ),
            "tag_slug": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Slug"
                }
            )
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('tag_slug')
        if not slug:
            name = self.cleaned_data.get('tag_name')
            if name:
                slug = slugify(name)
        return slug

    def clean_name(self):
        name = self.cleaned_data.get('tag_name')
        if Tag.objects.filter(tag_name=name).exists():
            raise forms.ValidationError("Esta etiqueta ya existe.")
        return name