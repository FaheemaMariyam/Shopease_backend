from django.urls import path
from .views import RegisterView,LoginView,logoutView,ProfileView,RefreshTokenView
from . import views
urlpatterns=[
    path("home/",views.home,name='home'),
    path("signup/",RegisterView.as_view(),name='signup'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',logoutView.as_view(),name='logout'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('token_refresh/',RefreshTokenView.as_view(),name='token_refresh'),
         
]