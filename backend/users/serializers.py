from django.contrib.auth import get_user_model

from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from recipes.models import Recipe

from .models import Subscribe

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField(default=False)

    class Meta:
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed'
                  )
        model = User

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.pk:
            return False
        if Subscribe.objects.filter(subscriber=user, author=obj).exists():
            return True
        return False


class UsersCreateSerializer(UserCreateSerializer):

    class Meta:
        fields = ('email', 'username', 'first_name', 'last_name', 'password',)
        model = User


class PartialRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class SubscribeSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )
        model = User
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_recipes(self, obj):
        limit = self.context['request'].query_params.get('recipes_limit', 3)
        queryset = obj.recipes.all()[:int(limit)]
        serializer = PartialRecipeSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
