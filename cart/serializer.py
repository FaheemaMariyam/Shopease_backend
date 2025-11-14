from rest_framework import serializers
from product.serializer import ProductSerializer
from .models import CartModel

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartModel
        fields = ['id', 'product', 'quantity', 'added_at']
