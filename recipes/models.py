from django.db import models
from django.utils.text import slugify
from products.models import Variety


class Ingredient(models.Model):
    """
    Data model: https://schema.org/RecipeIngredient
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    # TODO: Evaluar cómo vincular con variedades de productos.
    product = models.ForeignKey(Variety, blank=True, null=True, on_delete=models.SET_NULL)
    # Si no tenemos algún producto, puede quedar blank. Si sí está, vincular con el existente.

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Data model: https://schema.org/Category
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Data model: https://schema.org/DefinedTerm
    """

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Data model: https://schema.org/Recipe
    """

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
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


class RecipeIngredient(models.Model):
    """
    Data model: https://schema.org/RecipeIngredient
    """

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    unit = models.CharField(max_length=50)  # choices (cucharadita, tazas, ...)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ("recipe", "ingredient")

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name} for {self.recipe.name}"


class Step(models.Model):
    """
    Data model: https://schema.org/HowToStep
    """

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step_number = models.IntegerField()
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    photo = models.ImageField(upload_to="steps/", blank=True, null=True)

    class Meta:
        ordering = ["step_number"]

    def __str__(self):
        return f"Step {self.step_number} for {self.recipe.name}"
