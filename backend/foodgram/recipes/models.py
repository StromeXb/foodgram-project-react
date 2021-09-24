from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    """
    Класс для определения тэгов
    """
    name = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=7)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class MeasureUnit(models.Model):
    """
    Класс для единиц измерения
    """
    unit = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return self.unit


class Ingredient(models.Model):
    """
    Класс для ингредиетов
    """
    name = models.CharField(max_length=200, unique=True)
    measurement_unit = models.ForeignKey(MeasureUnit, on_delete=models.CASCADE, related_name='ingredients')

    def __str__(self):
        """при печати объекта выводится название"""
        return self.name


class Recipe(models.Model):
    """
    Класс для рецептов
    """
    tags = models.ManyToManyField(Tag, related_name='recipes')
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=200, unique=True)
    text = models.TextField()
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(1, 'This value must be an integer 1 or more'),
        ]
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class RecipeContent(models.Model):
    """
    Класс для содержания рецептов
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_content')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='recipe_content')
    amount = models.PositiveSmallIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'], name='unique ingredient per recipe'
            ),
        ]


class Favorite(models.Model):
    """
    класс для избранного
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorites')


class ShoppingCart(models.Model):
    """
    класс для покупок
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shopping_cart')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='shopping_cart')
