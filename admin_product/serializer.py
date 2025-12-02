# from rest_framework import serializers
# from product.models import Product, Category

# class AdminProductSerializer(serializers.ModelSerializer):
#     image = serializers.SerializerMethodField()  # add this

#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'image']

#     def get_image(self, obj):
#         if obj.image:
#             try:
#                 return obj.image.url  # CloudinaryField provides .url
#             except Exception:
#                 return None
#         return None
from rest_framework import serializers
from product.models import Product

class AdminProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'image']

    def get_image(self, obj):
        if obj.image:
            return obj.image.url.replace("http://", "https://")  # enforce HTTPS
        return None
