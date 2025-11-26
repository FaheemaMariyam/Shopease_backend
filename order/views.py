from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Order, OrderItem
from .serializer import OrderSerializer
from product.models import Product
import razorpay
from django.conf import settings

from django.db import transaction

def process_order(user, items, shipping, payment_method):
    total_price = 0
    order_items_list = []
    products_to_update = []

    with transaction.atomic(): #Either the entire order succeeds OR everything rolls back.Prevents:Partial stock decrease,incomplete orders
        for item in items:
            product = Product.objects.select_for_update().get(id=item["product_id"])#Locking-Locks the row in DB,Prevents two users buying same item at same time
            qty = item["quantity"]

            if qty <= 0:
                raise ValueError("Invalid quantity")

            if product.stock < qty:
                raise ValueError(f"Only {product.stock} left for {product.name}")

            price = product.price * qty
            total_price += price

            product.stock -= qty
            products_to_update.append(product)

            order_items_list.append({
                "product": product,
                "quantity": qty,
                "price": price
            })

        # bulk update stock
        Product.objects.bulk_update(products_to_update, ['stock'])

        order = Order.objects.create(
            user=user,
            total_price=total_price,
            payment_method=payment_method,
            name=shipping.get("name"),
            address=shipping.get("address"),
            city=shipping.get("city"),
            pin=shipping.get("pin"),
            phone=shipping.get("phone"),
            status="Pending"
        )

        OrderItem.objects.bulk_create([
            OrderItem(order=order, **oi) for oi in order_items_list
        ])

    return order

class OrderListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-id')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        items = data.get("items", [])
        if not items:
            return Response({"error": "No items provided"}, status=400)

        shipping = data.get("shippingDetails", {})

        try:
            order = process_order(
                user=request.user,
                items=items,
                shipping=shipping,
                payment_method=data.get("payment_method", "COD"),
            )
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        return Response(OrderSerializer(order).data, status=201)



class OrderStatusUpdateView(APIView):#Allows user to change status of THEIR OWN order to cancel (not admin).
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=400)
        # RESTORE STOCK IF ORDER IS CANCELLED
        if new_status == "Cancelled" and order.status != "Cancelled":
            for item in order.items.all():
                product = item.product
                if product: 
                    product.stock += item.quantity
                    product.save()
        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data)


class CreateRazorpayOrder(APIView):#Used before payment.
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
            #covert into paise(INR),create razorpay order
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


class VerifyRazorpayPayment(APIView):#Called after payment success.
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data

        # Razorpay details
        if not (data.get("razorpay_order_id") and data.get("razorpay_payment_id") and data.get("razorpay_signature")):
            return Response({"error": "Missing Razorpay payment details"}, status=400)

        # verify signature
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": data["razorpay_order_id"],
                "razorpay_payment_id": data["razorpay_payment_id"],
                "razorpay_signature": data["razorpay_signature"],
            })
        except:
            return Response({"error": "Invalid payment signature"}, status=400)

        shipping = data.get("shippingDetails", {})
        items = data.get("items", [])

        try:
            order = process_order(
                user=request.user,
                items=items,
                shipping=shipping,
                payment_method="RAZORPAY"
            )
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        return Response(OrderSerializer(order).data, status=201)
