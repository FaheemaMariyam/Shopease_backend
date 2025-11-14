from django.urls import path
from .views import CartView,CartItemDeleteView

urlpatterns=[
    path('cart/',CartView.as_view(),name='cart'),
    path('cart/<int:item_id>/',CartItemDeleteView.as_view(),name='cart-item-delete')

]