from django.urls import path
from .views import WishlistItemDeleteView,WishlistView

urlpatterns=[
    path('wishlist/',WishlistView.as_view(),name='wishlist'),
    path('wishlist/<int:item_id>',WishlistItemDeleteView.as_view(),name='wishlist-item-delete')
]