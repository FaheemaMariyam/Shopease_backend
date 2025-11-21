from rest_framework import serializers
from product.serializer import ProductSerializer
from shopease_user.serializer import UserProfileSerializer
from order.models import Order, OrderItem


class AdminOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]
        read_only_fields = ["id", "product", "quantity", "price"]


class AdminOrderSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    items = AdminOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "total_price",
            "payment_method",
            "status",
            "ordered_at",
            "name",
            "address",
            "city",
            "pin",
            "phone",
            "items",
        ]
        read_only_fields = [
            "id",
            "user",
            "total_price",
            "payment_method",
            "ordered_at",
            "name",
            "address",
            "city",
            "pin",
            "phone",
            "items",
        ]
