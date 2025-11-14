from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from product.models import Product
from .models import Wishlist
from .serializer import WishlistSerializer

class WishlistView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    #to get all the wishlist items
    def get(self,request):
        items=Wishlist.objects.filter(user=request.user).select_related('product')
        serializer=WishlistSerializer(items,many=True)
        return Response(serializer.data)
    #add items to wishlist
    def post(self,request):
        product_id=request.data.get("product_id")
        if not product_id:
            return Response({"error":"product id is required"},status=400)
        try:
            product=Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error":"product is required"},status=400)
        wishlist_item,created=Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )
        if not created:
            return Response({"message":"already in wishlist"},status=200)
        return Response(WishlistSerializer(wishlist_item).data,status=201)
    #clear entire wishlist
    def delete(self,request):
        Wishlist.objects.filter(user=request.user).delete()
        return Response({"message":"all items in wishlist were cleared"},status=204)
class WishlistItemDeleteView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    #delete single items(by id)
    def delete(self,request,item_id):
        deleted=Wishlist.objects.filter(id=item_id,user=request.user).delete()
        if deleted[0]:
            return Response({"message":"item removed from wishlist"},status=204)
        return Response({"error":"item not found"},status=404)

