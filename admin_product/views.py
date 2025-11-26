from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from product.models import Product
from product.serializer import ProductSerializer
from .serializer import AdminProductSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
import math

class AdminProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class AdminProductListView(APIView):
    permission_classes = [IsAdminUser]
    pagination_class = AdminProductPagination

    def get(self, request):
        products = Product.objects.all()

        # --- Search ---
        search = request.query_params.get("search")
        if search:
            products = products.filter(name__icontains=search)

        # --- Category filter ---
        category = request.query_params.get("category")
        if category:
            products = products.filter(category_id=category)

        # --- Sorting ---
        ordering = request.query_params.get("ordering")

        valid_ordering = ['price', '-price', 'name', '-name']

        if ordering in valid_ordering:
            products = products.order_by(ordering)
        else:
            products = products.order_by('-id')   # default

        # --- Pagination ---
        paginator = self.pagination_class()#Create paginator instance
        result_page = paginator.paginate_queryset(products, request)#Slice queryset for that page
        serializer = ProductSerializer(result_page, many=True)#Serialize only that page

        return paginator.get_paginated_response(serializer.data)

    def post(self,request):
        serializer=AdminProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"New product added", "product": serializer.data}, status=201)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class AdminProductDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        serializer = AdminProductSerializer(product)
        return Response(serializer.data)

    def patch(self, request, pk):
        product = get_object_or_404(Product, id=pk)

        serializer = AdminProductSerializer(
            product,
            data=request.data,
            partial=True #allow updates 1 field
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Product updated successfully",
                "product": serializer.data
            })
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return Response({"message": "Product deleted successfully"})
