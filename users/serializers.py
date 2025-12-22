from logging.config import valid_ident

from rest_framework import serializers
from .models import User, UserProfile
from djoser.serializers import UserSerializer, UserCreateSerializer


# UserProfile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["other_name", "date_of_birth", "phone_number"]


# CurrentUser Serializer
class CurrentUserSerializer(UserSerializer):
    user_profile = UserProfileSerializer(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = ["email", "first_name", "last_name", "role", "user_profile"]


# Registration Serializer (simple, no nested profile)
class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.is_active = True
        user.save()
        return user


class AdminUpdateRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["role"]
