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
    role = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "user_profile",
            "role",
        ]
        read_only_fields = ["id", "date_joined", "updated_at"]

    def get_role(self, obj) -> "str":
        if obj.is_owner:
            return "owner"
        if obj.is_customer:
            return "customer"
        return None


# Registration Serializer (simple, no nested profile)
class BaseRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["email", "password", "first_name", "last_name"]
