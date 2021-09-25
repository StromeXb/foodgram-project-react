from rest_framework import serializers
from .models import Ingredient, Recipe, RecipeContent, Tag
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class RecipeContentSerializer(serializers.ModelSerializer):

    name = serializers.StringRelatedField(read_only=True)
    measurement_unit = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = RecipeContent


class RecipeSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)
    author = UserSerializer(many=False, read_only=True)
    ingredients = RecipeContentSerializer(many=True, read_only=True)
    is_favorited = serializers.SlugField()
    is_in_shopping_cart = serializers.SlugField()

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
