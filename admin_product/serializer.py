
from rest_framework import serializers
from product.models import Product,Category

class AdminProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'image']

# Now 'category' can accept an ID
