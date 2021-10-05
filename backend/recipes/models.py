from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """
    Класс для определения тэгов
    """
    name = models.CharField(
        verbose_name='Название тэга',
        max_length=200,
        unique=True
    )
    color = models.CharField(verbose_name='Код цвета', max_length=7)
    slug = models.SlugField(
        verbose_name='Код тэга',
        max_length=200,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class MeasureUnit(models.Model):
    """
    Класс для единиц измерения
    """
    unit = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return self.unit

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'


class Ingredient(models.Model):
    """
    Класс для ингредиетов
    """
    name = models.CharField(verbose_name='Ингредиент', max_length=200)
    measurement_unit = models.ForeignKey(
        MeasureUnit,
        verbose_name='Единицы измерения',
        on_delete=models.CASCADE,
        related_name='ingredients'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique ingredient and measure'
            ),
        ]

    def __str__(self):
        """при печати объекта выводится название"""
        return self.name


class Recipe(models.Model):
    """
    Класс для рецептов
    """
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name='recipes'
    )
    image = models.ImageField(verbose_name='Картинка', upload_to='images/')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeContent',
        verbose_name='Ингредиенты'
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200,
        unique=True
    )
    text = models.TextField(verbose_name='Описание рецепта')
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        # validators=[
        #     MinValueValidator(1, message=('Время приготовления должно ' +
        #                                   'быть 1 минута или больше')),
        # ]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeContent(models.Model):
    """
    Класс для содержания рецептов
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_content',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_content',
        verbose_name='Ингредиент'
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        # default=0,
        # validators=[
        #     MinValueValidator(1, message=('Количество должно ' +
        #                                   'быть 1 или больше')),
        # ]
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique ingredient per recipe'
            ),
        ]


class Favorite(models.Model):
    """
    класс для избранного
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт в избранном'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique user per recipe in favorites'
            ),
        ]


class ShoppingCart(models.Model):
    """
    класс для покупок
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт в корзине'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique user per recipe in shopping cart'
            ),
        ]
