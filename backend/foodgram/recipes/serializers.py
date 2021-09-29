from rest_framework import serializers
from .models import Ingredient, Recipe, RecipeContent, Tag, Favorite
from users.serializers import UserSerializer

import base64

from django.core.files.base import ContentFile


class Base64ImageField(serializers.ImageField):
    def from_native(self, data):
        if isinstance(data, basestring) and data.startswith('data:image'):
            # base64 encoded image - decode
            format, imgstr = data.split(';base64,')  # format ~= data:image/X,
            ext = format.split('/')[-1]  # guess file extension

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super(Base64ImageField, self).from_native(data)


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
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = serializers.CharField(read_only=True, source='ingredient.measurement_unit')

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount', )
        model = RecipeContent


class RecipeSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)
    author = UserSerializer(many=False, read_only=True)
    ingredients = RecipeContentSerializer(source='recipe_content', many=True)
    is_favorited = serializers.SlugField(required=False)
    is_in_shopping_cart = serializers.SlugField(required=False)
    image = Base64ImageField(use_url=True, max_length=None)

    class Meta:
        model = Recipe
        fields = (
            'id',
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

    def create(self, validated_data):
        contents = validated_data.pop('contents')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe.save()
        for item in contents:
            content = RecipeContentSerializer(item).data
            amount = content['amount']
            ingredient_id = content['id']
            ingredient = Ingredient.objects.get(pk=ingredient_id)
            content = RecipeContent.objects.create(
                recipe=recipe,
                ingredient=ingredient, amount=amount
            )
            content.save()
        return recipe

    def update(self, instance, validated_data):
        contents = validated_data.pop('contents')
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        instance.ingredients.clear()
        for item in contents:
            content = RecipeContentSerializer(item).data
            amount = content['amount']
            ingredient_id = content['id']
            ingredient = Ingredient.objects.get(pk=ingredient_id)
            content = RecipeContent.objects.create(
                recipe=instance,
                ingredient=ingredient, amount=amount
            )
            content.save()
        return instance
