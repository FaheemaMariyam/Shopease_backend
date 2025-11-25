from django.urls import path
from .views import (
    CategoryListView,
    ProductListView,
    ProductDetailsView,
    ProductsByCategoryView,
    
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product-detail'),
    path('categories/<int:pk>/products/', ProductsByCategoryView.as_view(), name='products-by-category'),
    
]
