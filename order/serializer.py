from rest_framework import serializers
from .models import Order, OrderItem
from product.serializer import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'total_price', 'payment_method', 
            'status', 'ordered_at', 'name', 'address', 
            'city', 'pin', 'phone', 'items'
        ]
        read_only_fields = ['user', 'status', 'ordered_at']
