from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Order, OrderItem
from .serializer import OrderSerializer
from product.models import Product

class OrderListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """List all orders for the logged-in user"""
        orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create an order.
        Accepts payload like:
        {
            "items": [
                {"product_id": 1, "quantity": 2},
                {"product_id": 3, "quantity": 1}
            ],
            "payment_method": "COD",
            "name": "...",
            "address": "...",
            "city": "...",
            "pin": "...",
            "phone": "..."
        }
        """
        data = request.data
        items = data.get('items', [])
        if not items:
            return Response({"error": "No items provided"}, status=status.HTTP_400_BAD_REQUEST)

        total_price = 0
        order_items = []

        for item in items:
            try:
                product = Product.objects.get(id=item['product_id'])
            except Product.DoesNotExist:
                return Response({"error": f"Product {item['product_id']} not found"}, status=404)

            quantity = item.get('quantity', 1)
            price = product.price * quantity
            total_price += price

            order_items.append({
                "product": product,
                "quantity": quantity,
                "price": price
            })

        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            payment_method=data.get('payment_method', 'COD'),
            name=data.get('name', ''),
            address=data.get('address', ''),
            city=data.get('city', ''),
            pin=data.get('pin', ''),
            phone=data.get('phone', '')
        )

        for oi in order_items:
            OrderItem.objects.create(order=order, **oi)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, order_id):
        """
        Update order status (like canceling)
        Payload: {"status": "Cancelled"}
        """
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=400)

        order.status = new_status
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
