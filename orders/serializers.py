from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "menu_item", "quantity", "price", "created_at", "updated_at"]
        read_only_fields = ["id", "updated_at", "created_at"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "order_date",
            "status",
            "total_amount",
            "order_items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["updated_at", "created_at", "status", "total_amount"]
