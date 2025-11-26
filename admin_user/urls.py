from django.urls import path
from .views import AdminUserListView,AdminDetailView,AdminUserDetailView

urlpatterns=[
    path('admin/users/',AdminUserListView.as_view(),name='admin_users'),
    path('admin/users/<int:pk>/',AdminDetailView.as_view(),name='admin_user_manage'),
    path('admin/users/<int:pk>/details/',AdminUserDetailView.as_view(),name='admin_user_details'),
]