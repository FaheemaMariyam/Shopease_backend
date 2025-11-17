from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from product.models import Product
from .models import CartModel
from .serializer import CartSerializer

class CartView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    #list all  cart items
    def get(self,request):
        items=CartModel.objects.filter(user=request.user).select_related("product")
        serializer=CartSerializer(items,many=True)
        return Response(serializer.data)
    def post(self, request):
        #Add new item or increase quantity
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if not product_id:
            return Response({"error": "product_id is required"}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        cart_item, created = CartModel.objects.get_or_create(
            user=request.user, product=product
        )

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        return Response(CartSerializer(cart_item).data, status=200)
    

    #delete the entire cart
    def delete(self,request):
        CartModel.objects.filter(user=request.user).delete()
        return Response({"message": "Cart cleared"}, status=204)

#remove or edit a single cart item based on id
class CartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, item_id):
        # Increase or decrease quantity
        cart_item = CartModel.objects.get(id=item_id, user=request.user)
        delta = int(request.data.get("delta", 0))
        cart_item.quantity += delta
        if cart_item.quantity < 1:
            cart_item.quantity = 1
        cart_item.save()
        return Response(CartSerializer(cart_item).data)

    def delete(self, request, item_id):
        # Remove single item
        deleted = CartModel.objects.filter(id=item_id, user=request.user).delete()
        if deleted[0]:
            return Response({"message": "Item deleted successfully"}, status=204)
        return Response({"error": "Item not found"}, status=404)
