from django.contrib import admin

from .models import (Favorite, Ingredient, MeasureUnit, Recipe, RecipeContent,
                     Tag)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Страница админ. панели рецепов."""

    list_display = (
        'pk',
        'name',
        'image',
        'text',
        'author',
        'cooking_time'
    )
    search_fields = ('name', 'tags', 'author',)
    list_filter = ('tags',)
    empty_value_display = '-пусто-'


@admin.register(RecipeContent)
class RecipeContentAdmin(admin.ModelAdmin):
    """Страница админ. панели содержания рецепов."""

    list_display = (
        'pk',
        'recipe',
        'ingredient',
        'amount'
    )
    search_fields = ('recipe', 'ingredient',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Страница админ. панели тагов."""

    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name', 'slug',)
    empty_value_display = '-пусто-'


@admin.register(MeasureUnit)
class MeasureUnitAdmin(admin.ModelAdmin):
    """Страница админ. панели тагов."""

    list_display = (
        'pk',
        'unit',
    )
    search_fields = ('unit',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Страница админ. панели тагов."""

    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Страница админ. панели избранного."""

    list_display = (
        'user',
        'recipe',
    )
    empty_value_display = '-пусто-'
