from rest_framework import serializers
from product.serializer import ProductSerializer
from shopease_user.serializer import UserProfileSerializer
from order.models import Order, OrderItem


class AdminOrderItemSerializer(serializers.ModelSerializer):#for each single order
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]
        read_only_fields = ["id", "product", "quantity", "price"]


class AdminOrderSerializer(serializers.ModelSerializer):#Shows full customer order details
    user = UserProfileSerializer(read_only=True)
    items = AdminOrderItemSerializer(many=True, read_only=True)#show all order of the same user
    status = serializers.CharField(default="Pending")
    
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
