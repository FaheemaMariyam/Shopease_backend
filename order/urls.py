from django.urls import path
from .views import OrderListCreateView,OrderStatusUpdateView

urlpatterns=[
    path('orders/',OrderListCreateView.as_view(),name='order'),
    path('orders/<int:order_id>/status/',OrderStatusUpdateView.as_view(),name='order-status-update')
]