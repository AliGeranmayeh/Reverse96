from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import LoginSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.core.mail import send_mail


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = CustomUser.objects.get(id=user_data.get('id'))
        access_tk = str(AccessToken.for_user(user))
        refresh_tk = str(RefreshToken.for_user(user))
        return Response({"message": serializer.data,
                         "access": access_tk,
                         "refresh": refresh_tk},
                         status=status.HTTP_201_CREATED)
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        user = CustomUser.objects.filter(Q(username=username)|Q(email=username)).first()
        if not user or not check_password(password, user.password):
            return Response ({"message": "Invalid user"}, status=status.HTTP_404_NOT_FOUND)
        access_tk = str(AccessToken.for_user(user))
        refresh_tk = str(RefreshToken.for_user(user))
        return Response(data={"access": access_tk, "refresh": refresh_tk}, status=status.HTTP_200_OK)


