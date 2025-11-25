from django.shortcuts import render
from rest_framework import generics,filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category,Product
from .serializer import CategorySerializer,ProductSerializer
import math


#custom pagination with full information
class ProductPagination(PageNumberPagination):
    page_size = 10
    def get_paginated_response(self, data):
        total_items = self.page.paginator.count
        total_pages = math.ceil(total_items / self.page_size)
        return Response({
            'total_items': total_items,
            'total_pages': total_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
#list all categories
class CategoryListView(generics.ListAPIView):
    queryset=Category.objects.all().order_by("name")
    serializer_class=CategorySerializer
    permission_classes=[IsAuthenticatedOrReadOnly]

#list all products with pagination,filter,search,sort
class ProductListView(generics.ListAPIView):
    queryset=Product.objects.all().order_by("-id")
    serializer_class=ProductSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    pagination_class=ProductPagination

    filter_backends=[DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]

    filterset_fields=['category','category__name']

    search_fields=['name','description']

    ordering_fields=['price','name']

#view single product by id
class ProductDetailsView(generics.RetrieveAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]

# List products by category ID (extra endpoint)
class ProductsByCategoryView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = ProductPagination

    def get_queryset(self):
        category_id = self.kwargs['pk']
        return Product.objects.filter(category_id=category_id).order_by("-id")


