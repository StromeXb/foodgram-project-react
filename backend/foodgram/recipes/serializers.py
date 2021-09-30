import base64
import imghdr
import uuid

import six
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.serializers import UserSerializer

from .models import Ingredient, Recipe, RecipeContent, Tag


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:20]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


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
        if self.context.get('request').method == 'POST':
            if attrs['amount'] < 1:
                raise serializers.ValidationError(
                    'Amount must be greater then 1'
                )
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
        if self.context.get('request').method == 'POST':
            if attrs['cooking_time'] < 1:
                raise serializers.ValidationError(
                    'Cooking time must be greater then 1'
                )
        return attrs

    def create(self, validated_data):
        ingredients = validated_data.pop('recipe_content')
        tags = validated_data.pop('tags')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(**validated_data, author=author)
        recipe.tags.set(tags)
        recipe.save()
        for item in ingredients:
            content = RecipeContentSerializer(item).data
            amount = content['amount']
            ingredient_id = content['id']
            ingredient = Ingredient.objects.get(pk=ingredient_id)
            content = RecipeContent.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount
            )
            content.save()
        return recipe

    def update(self, instance, validated_data):
        contents = validated_data.pop('recipe_content')
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
                ingredient=ingredient,
                amount=amount
            )
            content.save()
        return instance
