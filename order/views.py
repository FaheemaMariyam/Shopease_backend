from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Order, OrderItem
from .serializer import OrderSerializer
from product.models import Product
import razorpay
from django.conf import settings


class OrderListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        items = data.get('items', [])

        if not items:
            return Response({"error": "No items provided"}, status=400)

        total_price = 0
        order_items_list = []

        # for item in items:
        #     try:
        #         product = Product.objects.get(id=item['product_id'])
        #     except Product.DoesNotExist:
        #         return Response({"error": f"Product {item['product_id']} not found"}, status=404)

        #     qty = item.get('quantity', 1)
        #     price = product.price * qty
        #     total_price += price

        #     order_items_list.append({
        #         "product": product,
        #         "quantity": qty,
        #         "price": price
        #     })
        for item in items:
            try:
                product = Product.objects.get(id=item["product_id"])
            except Product.DoesNotExist:
                return Response({"error": "Product not found"}, status=404)

            qty = item["quantity"]
            price = product.price * qty
            total_price += price

    # decrease stock here
            if product.stock < qty:
                return Response({"error": f"Sorry, Only {product.stock} left for {product.name}"}, status=400)

            product.stock -= qty
            product.save()

            order_items_list.append({
                "product": product,
                "quantity": qty,
                "price": price
            })


        shipping = data.get("shippingDetails", {})

        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            payment_method=data.get('payment_method', 'COD'),
            name=shipping.get("name"),
            address=shipping.get("address"),
            city=shipping.get("city"),
            pin=shipping.get("pin"),
            phone=shipping.get("phone"),
    )




        #  BULK CREATE ORDER ITEMS (optimized)
        OrderItem.objects.bulk_create([
            OrderItem(order=order, **oi) for oi in order_items_list
        ])

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=201)


class OrderStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=400)

        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data)


class CreateRazorpayOrder(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            amount = request.data.get("amount")

            if amount is None:
                return Response({"error": "Amount is required"}, status=400)

            try:
                amount = float(amount)
            except:
                return Response({"error": "Invalid amount"}, status=400)

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            rzp_order = client.order.create({
                "amount": int(amount * 100),
                "currency": "INR",
                "payment_capture": 1
            })

            return Response({
                "order_id": rzp_order["id"],
                "amount": rzp_order["amount"],
                "currency": rzp_order["currency"],
                "key_id": settings.RAZORPAY_KEY_ID
            })

        except Exception:
            return Response({"error": "Failed to create Razorpay order"}, status=500)


class VerifyRazorpayPayment(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data

        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_signature = data.get("razorpay_signature")
        items = data.get("items")
        # shipping = data.get("shippingDetails", {})
        shipping = data.get("shippingDetails", {})

        name = shipping.get("name")
        address = shipping.get("address")
        city = shipping.get("city")
        pin = shipping.get("pin")
        phone = shipping.get("phone")


        if not (razorpay_order_id and razorpay_payment_id and razorpay_signature):
            return Response({"error": "Missing Razorpay payment details"}, status=400)

        # Verify Razorpay signature
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            })
        except:
            return Response({"error": "Invalid payment signature"}, status=400)

        total_price = 0
        order_items_list = []

        # for item in items:
        #     try:
        #         product = Product.objects.get(id=item["product_id"])
        #     except Product.DoesNotExist:
        #         return Response({"error": "Product not found"}, status=404)

        #     qty = item["quantity"]
        #     price = product.price * qty
        #     total_price += price

        #     order_items_list.append({
        #         "product": product,
        #         "quantity": qty,
        #         "price": price
        #     })
        for item in items:
            try:
                product = Product.objects.get(id=item["product_id"])
            except Product.DoesNotExist:
                return Response({"error": "Product not found"}, status=404)

            qty = item["quantity"]
            price = product.price * qty
            total_price += price

    # 🔥 decrease stock here
            if product.stock < qty:
                return Response({"error": f"Only {product.stock} left for {product.name}"}, status=400)

            product.stock -= qty
            product.save()

            order_items_list.append({
                "product": product,
                "quantity": qty,
                "price": price
            })


        # order = Order.objects.create(
        #     user=request.user,
        #     total_price=total_price,
        #     payment_method="RAZORPAY",
        #     name=shipping.get("name"),
        #     address=shipping.get("address"),
        #     city=shipping.get("city"),
        #     pin=shipping.get("pin"),
        #     phone=shipping.get("phone"),
        #     status="Pending"
        # )
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            payment_method="RAZORPAY",
            name=name,
            address=address,
            city=city,
            pin=pin,
            phone=phone,
            status="Pending"
)


        #  BULK CREATE USED HERE ALSO
        OrderItem.objects.bulk_create([
            OrderItem(order=order, **oi) for oi in order_items_list
        ])

        return Response(OrderSerializer(order).data, status=201)
