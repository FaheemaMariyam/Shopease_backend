from django.urls import path
from .views import AdminOrderListView,AdminStatusUpdateView

urlpatterns=[
    path('admin/orders/',AdminOrderListView.as_view(),name='admin_orders'),
    path('admin/orders/<int:pk>/status/',AdminStatusUpdateView.as_view(),name='admin_status')
]