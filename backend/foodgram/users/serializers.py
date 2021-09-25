from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.BooleanField(default=False)

    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')
        model = User
