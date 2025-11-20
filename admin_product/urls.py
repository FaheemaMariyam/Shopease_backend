from django.urls import path
from .views import AdminProductListView,AdminProductDetailView

urlpatterns=[
    path('admin/products/',AdminProductListView.as_view(),name='admin_product'),
    path('admin/products/<int:pk>/',AdminProductDetailView.as_view(),name='admin_product_details')
]