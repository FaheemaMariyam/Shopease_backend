from rest_framework import serializers
from shopease_user.models import User
from order.models import Order, OrderItem

class AdminOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["product_name", "quantity", "price"]
        read_only_fields = ["product_name", "quantity", "price"]

    def get_product_name(self, obj):
        # Return product name or fallback if product deleted
        return obj.product.name if obj.product else "Product deleted"

class AdminOrderSerializer(serializers.ModelSerializer):
    items = AdminOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "status", "total_price", "payment_method", "ordered_at", "items"]
        read_only_fields = ["id", "status", "total_price", "payment_method", "ordered_at", "items"]

class AdminUserDetailSerializer(serializers.ModelSerializer):
    orders = AdminOrderSerializer(many=True, read_only=True, source="order_set")

    class Meta:
        model = User
        fields = [
            "id", "name", "email", "phone", "address", "pin", "blocked", "date_joined", "orders"
        ]
        read_only_fields = [
            "id", "name", "email", "phone", "address", "pin", "blocked", "date_joined", "orders"
        ]
