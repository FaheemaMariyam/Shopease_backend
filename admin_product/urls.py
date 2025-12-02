from django.urls import path
from .views import AdminProductListView,AdminProductDetailView,CategoryUpdateView

urlpatterns=[
    path('admin/products/',AdminProductListView.as_view(),name='admin_product'),
    path('admin/products/<int:pk>/',AdminProductDetailView.as_view(),name='admin_product_details'),
    path('admin/categories/<int:pk>/', CategoryUpdateView.as_view(),name='admin_category_update'),
]