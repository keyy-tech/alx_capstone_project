from rest_framework import serializers
from .models import Restaurants, Menu


class MenuSerializers(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "name",
            "description",
            "price",
            "is_available",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class RestaurantsSerializers(serializers.ModelSerializer):
    menu = MenuSerializers(many=True, read_only=True)

    class Meta:
        model = Restaurants
        fields = [
            "name",
            "description",
            "address",
            "phone_number",
            "menu",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
