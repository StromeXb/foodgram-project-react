from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, ParseError

from users.serializers import UserSerializer
from .fields import Base64ImageField
from .models import Ingredient, Recipe, RecipeContent, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag

    def to_internal_value(self, data):
        if not isinstance(data, int):
            message = self.error_messages['invalid'].format(
                datatype=type(data).__name__
            )
            raise ValidationError({
                'tags': [message]
            }, code='invalid')
        return data


class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class RecipeContentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = serializers.CharField(
        read_only=True, source='ingredient.measurement_unit'
    )

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount', )
        model = RecipeContent

    def validate(self, attrs):
        if self.context.get('request').method in ('POST', 'PUT', 'PATCH'):
            if attrs['amount'] < 1:
                ingredient = get_object_or_404(
                    Ingredient, id=attrs['ingredient']['id'])
                error_data = {'amount': ['Количество для ингредиента '
                                         f'{ingredient.name} должно быть больше 0.']}
                raise ParseError(error_data)
        return attrs


class RecipeSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)
    author = UserSerializer(many=False, read_only=True)
    ingredients = RecipeContentSerializer(source='recipe_content', many=True)
    is_favorited = serializers.BooleanField(
        default=False,
        required=False,
        read_only=True
    )
    is_in_shopping_cart = serializers.BooleanField(
        default=False,
        required=False,
        read_only=True
    )
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

    def validate(self, attrs):
        if self.context.get('request').method in ('POST', 'PUT', 'PATCH'):
            if attrs['cooking_time'] < 1:
                raise serializers.ValidationError(
                    'Время приготовления должно быть больше 0'
                )
            if not attrs['tags']:
                raise serializers.ValidationError(
                    'Укажите тэги, пожалуйста.'
                )
            if not attrs.get('recipe_content'):
                raise serializers.ValidationError(
                    'Добавьте хотя бы 1 ингредиент'
                )
            ing_list = []
            for ingredients in attrs.get('recipe_content'):
                ing_list.append(ingredients['ingredient']['id'])

            for ing in ing_list:
                if ing_list.count(ing)>1:
                    ingredient = get_object_or_404(Ingredient, id=ing)
                    error_data = {'ingredients': [
                        f'Ингредиенты {ingredient.name} повторяются, '
                        'пожалуйста, укажите уникальные.'
                    ]
                    }
                    raise ParseError(error_data)

            # if len(list(ing_list)) > len(set(ing_list)):
            #     raise serializers.ValidationError(
            #         'Ингредиенты повторяются, пожалуйста, укажите уникальные.'
            #     )
            for ing in attrs.get('recipe_content'):
                if int(ing['amount']) < 1:
                    ingredient = get_object_or_404(
                        Ingredient, id=attrs['ingredient']['id'])
                    error_data = {'amount': ['Количество для ингредиента '
                                  f'{ingredient.name} должно быть больше 0.']}
                    raise ParseError(error_data)
        return attrs

    def create_or_update(self, validated_data, instance=None):
        args = locals()
        contents = validated_data.pop('recipe_content')
        tags = validated_data.pop('tags')
        if instance:
            instance = args['instance']
            instance.name = validated_data.get('name', instance.name)
            instance.text = validated_data.get('text', instance.text)
            instance.cooking_time = validated_data.get(
                'cooking_time', instance.cooking_time
            )
            instance.image = validated_data.get('image', instance.image)
        else:
            author = self.context.get('request').user
            instance = Recipe.objects.create(**validated_data, author=author)
        instance.tags.set(tags)
        instance.save()
        instance.ingredients.clear()
        for item in contents:
            content = RecipeContentSerializer(item).data
            amount = content['amount']
            ingredient_id = content['id']
            ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
            content = RecipeContent.objects.create(
                recipe=instance,
                ingredient=ingredient,
                amount=amount
            )
            content.save()
        return instance

    def create(self, validated_data):
        return self.create_or_update(validated_data)

    def update(self, instance, validated_data):
        return self.create_or_update(
            instance=instance,
            validated_data=validated_data
        )
