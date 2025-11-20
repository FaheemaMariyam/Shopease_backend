from django.urls import path
from .views import OrderListCreateView,OrderStatusUpdateView,CreateRazorpayOrder,VerifyRazorpayPayment

urlpatterns=[
    path('orders/',OrderListCreateView.as_view(),name='order'),
    path('orders/<int:order_id>/status/',OrderStatusUpdateView.as_view(),name='order-status-update'),
     path("orders/razorpay/create-order/", CreateRazorpayOrder.as_view(), name="razorpay-create-order"),
     path("orders/razorpay/verify-payment/", VerifyRazorpayPayment.as_view()),
]