from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from users.models import Subscribe

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(subscriber=user, author=obj).exists()
