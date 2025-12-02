from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Serve correct Cloudinary HTTPS URL
        if instance.image:
            try:
                data["image"] = instance.image.url.replace("http://", "https://")
            except:
                data["image"] = None
        else:
            data["image"] = None

        return data



class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            try:
                return obj.image.url.replace("http://", "https://")
            except Exception:
                return None
        return None
