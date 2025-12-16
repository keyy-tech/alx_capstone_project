from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            "cart",
            "menu_item",
            "quantity",
            "price",
            "added_at",
        ]
        read_only_fields = ["added_at"]


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Cart
        fields = [
            "total_price",
            "cart_items",
            "added_at",
            "updated_at",
        ]
        read_only_fields = ["total_price", "added_at", "updated_at"]
