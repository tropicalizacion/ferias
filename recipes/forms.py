from django import forms
from .models import Recipe, RecipeIngredient, Step, Tag


"""
class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    # image = models.ImageField(upload_to="recipes/", blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
"""


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
            "name",
            "description",
            "category",
            "tags",
        ]  # Estos son los campos que se incluyen en el formulario. No se incluye slug porque ese se crea automáticamente.


"""
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES, default="unit")
    quantity = models.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        unique_together = ("recipe", "ingredient")

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name} for {self.recipe.name}"
"""


class RecipeIngredientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ingredient"].empty_label = "Seleccione un ingrediente..."
        self.fields["unit"].choices = RecipeIngredient.UNIT_CHOICES

    class Meta:
        model = RecipeIngredient
        fields = ["ingredient", "unit", "quantity"]


# Cada receta va a tener varias instancias de RecipeIngredientForm.
# forms.inlineformset_factory() permite crear un conjunto de formularios (formset) relacionados a un modelo padre por medio del foreign key.
RecipeIngredientFormSet = forms.inlineformset_factory(
    Recipe,  # Modelo padre.
    RecipeIngredient,  # Modelo hijo.
    form=RecipeIngredientForm,  # Formulario a desplegar.
    extra=1,  # Mostrar un formulario extra inicialmente.
)


"""
class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step_sequence = models.IntegerField()
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    photo = models.ImageField(upload_to="steps/", blank=True, null=True)

    class Meta:
        ordering = ["step_sequence"]

    def __str__(self):
        return f"Step {self.step_sequence} for {self.recipe.name}"
"""


class StepForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["step_sequence"].widget.attrs.update(
            {"min": 1}
        )  # Debe tener al menos un paso.

    class Meta:
        model = Step
        fields = [
            "step_sequence",
            "title",
            "description",
            "photo",
        ]


# Cada receta va a tener varias instancias de StepForm.
StepFormSet = forms.inlineformset_factory(
    Recipe,  # Modelo padre.
    Step,  # Modelo hijo.
    form=StepForm,  # Formulario a desplegar.
    extra=1,  # Mostrar un formulario extra inicialmente.
)
