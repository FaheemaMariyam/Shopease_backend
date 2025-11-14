from rest_framework import serializers
from .models import Wishlist
from product.serializer import ProductSerializer

class WishlistSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)
    class Meta:
        model=Wishlist
        fields=['id','product','added_at']