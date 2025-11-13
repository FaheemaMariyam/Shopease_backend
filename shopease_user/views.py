from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response  import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import RegisterSerializer,UserProfileSerializer
from .models import User

class RegisterView(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"user registered successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    #login(jwt+cookies)
class LoginView(APIView):
    def post(self,request):
        email=request.data.get("email")
        password=request.data.get("password")
        user = authenticate(username=email, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if user.blocked:
            return Response({"detail": "Your account is blocked"}, status=status.HTTP_403_FORBIDDEN)
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({
            "message": "Login successful",
            "user": UserProfileSerializer(user).data,
        }, status=status.HTTP_200_OK)
             # Set cookies (JWT stored securely)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,   # change to True in production (HTTPS)
            samesite="Lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="Lax",
        )

        return response

        
#logout(delete jwt cookies)
class logoutView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
class ProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
        serializer=UserProfileSerializer(user)
        return Response(serializer.data)
# REFRESH TOKEN
class RefreshTokenView(APIView):
    def post(self, request):
        from rest_framework_simplejwt.tokens import RefreshToken, TokenError

        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"detail": "No refresh token provided"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = Response({"access_token": access_token}, status=status.HTTP_200_OK)
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,
                samesite="Lax",
            )
            return response
        except TokenError:
            return Response({"detail": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
def home(request):
    return HttpResponse("This is home page")
