
# from rest_framework import serializers
# from product.models import Product,Category

# class AdminProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'image']
# #used new serializer instead of product serializer bcz, in product serializer stock=read only,but admin need to change the stock
# # Now 'category' can accept an ID
from rest_framework import serializers
from product.models import Product, Category

class AdminProductSerializer(serializers.ModelSerializer):
    # Ensure category is writeable via primary key
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'image']
