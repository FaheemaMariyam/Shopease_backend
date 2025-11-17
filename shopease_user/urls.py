from django.urls import path
from .views import RegisterView,LoginView,LogoutView,ProfileView
from . import views
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns=[
    
    path("signup/",RegisterView.as_view(),name='signup'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
         
]