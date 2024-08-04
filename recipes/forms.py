from django import forms
from .models import Recipe, RecipeIngredient, Step, Tag, Ingredient, Variety


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
                attrs={"class": "form-control", "placeholder": "Introduzca un nombre"}
            ),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control", "size": 5}),
        }


# TODO: Debe haber un espacio donde el usuario pueda crear un nuevo ingrediente (que no esté en la lista de ingredientes que se despliega).
class RecipeIngredientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ingredient"].empty_label = "Seleccione un ingrediente..."
        self.fields["unit"].choices = RecipeIngredient.UNIT_CHOICES

    class Meta:
        model = RecipeIngredient
        fields = ["id", "ingredient", "unit", "quantity"]
        widgets = {
            "id": forms.HiddenInput(),
            "ingredient": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "unit": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Cantidad",
                    "min": 0,
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
                    "placeholder": "Introduzca un número",
                    "min": 1,
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Introduzca un título",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
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
    class Meta:
        model = Ingredient
        fields = [
            "name",
            "description",
            "product",
            "is_vegetarian",
            "is_vegan",
            "is_gluten_free",
            "is_dairy_free",
            "is_nut_free",
            "is_soy_free",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "product": forms.Select(
                attrs={
                    "class": "form-control",
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
