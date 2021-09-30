from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from recipes.models import Recipe

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.BooleanField(default=False)

    class Meta:
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed'
                  )
        model = User


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
            'username', 'email', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )
        model = User
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_recipes(self, obj):
        recipes_limit = 10
        try:
            recipes_limit = self.context[
                'request'
            ].query_params['recipes_limit']
        except Exception:
            pass
        queryset = obj.recipes.all()[:int(recipes_limit)]
        serializer = PartialRecipeSerializer(queryset, many=True)
        return serializer.data
    
    def get_recipes_count(self, obj):
        return obj.recipes.count()
