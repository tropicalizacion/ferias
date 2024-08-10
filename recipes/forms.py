from django import forms
from django.utils.text import slugify
from .models import Recipe, RecipeIngredient, Step, Tag, Ingredient, Category, Tag, Variety


class RecipeForm(forms.ModelForm):
    # Esto va a desplegar todas las etiquetas que ya están en la base de datos.
    # PREGUNTA: ¿El usuario va a poder agregar tags nuevos?
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].empty_label = "Seleccione una categoría..."

    class Meta:
        model = Recipe  # El tipo de modelo asociado al formulario.
        fields = [
            "id",
            "name",
            "description",
            "category",
            "tags",
        ]  # Estos son los campos que se incluyen en el formulario. No se incluye slug porque ese se crea automáticamente.
        widgets = {
            "id": forms.HiddenInput(),
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-check-inline", "size": 5}),
        }


# TODO: Debe haber un espacio donde el usuario pueda crear un nuevo ingrediente (que no esté en la lista de ingredientes que se despliega).
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ingredient_product"].empty_label = "Seleccione un producto..."
        self.fields["ingredient_name"].widget.attrs.update({
            "placeholder": "Nombre",
        })

        self.fields["ingredient_name"].required = False
        self.fields["ingredient_description"].required = False
        self.fields["ingredient_product"].required = False
        self.fields["is_vegetarian"].required = False
        self.fields["is_vegan"].required = False
        self.fields["is_gluten_free"].required = False
        self.fields["is_dairy_free"].required = False
        self.fields["is_nut_free"].required = False
        self.fields["is_soy_free"].required = False

    class Meta:
        model = Ingredient
        fields = [
            "ingredient_name",
            "ingredient_description",
            "ingredient_product",
            "is_vegetarian",
            "is_vegan",
            "is_gluten_free",
            "is_dairy_free",
            "is_nut_free",
            "is_soy_free",
        ]
        widgets = {
            "ingredient_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del ingrediente",
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
            "is_vegetarian": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "is_vegan": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "is_gluten_free": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "is_dairy_free": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "is_nut_free": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "is_soy_free": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
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