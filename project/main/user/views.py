from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import LoginSerializer, RegisterSerializer,EmailActivisionSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser,EmailValidation
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.core.mail import send_mail
from random import seed
from random import randint

def randomNumber():
    value = randint(1000, 9999)
    return value


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = CustomUser.objects.get(id=user_data.get('id'))
        user_code = randomNumber()
        email_validation= EmailValidation.objects.create(email=user.email, code=user_code)
        #access_tk = str(AccessToken.for_user(user))
        #refresh_tk = str(RefreshToken.for_user(user))
        subject = 'welcome to Reverse96'
        message = f'Hi {user.username}, thank you for registering. please enter this code to our website: {user_code}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, email_from, recipient_list, fail_silently=False)
        return Response({"message": serializer.data}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        user = CustomUser.objects.filter(Q(username=username)|Q(email=username)).first()
        user_obj = CustomUser.objects.get(Q(username=username)|Q(email=username))
        if not user:
            return Response({"message": "invalid username or email"}, status=status.HTTP_404_NOT_FOUND)
        if not check_password(password, user.password):
            return Response({"message": "wrong password"}, status=status.HTTP_404_NOT_FOUND)
        if not user_obj.is_active:
            return Response({"message": "validate your email"}, status=status.HTTP_403_FORBIDDEN)
        access_tk = str(AccessToken.for_user(user))
        refresh_tk = str(RefreshToken.for_user(user))
        return Response(data={"access": access_tk, "refresh": refresh_tk}, status=status.HTTP_200_OK)


class EmailActivisionView(APIView):
    def get(self,request):
        serializer= EmailActivisionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        code = serializer.validated_data.get("code")
        email = serializer.validated_data.get("email")
        user= EmailValidation.objects.get(email=email)
        #user_code= EmailValidation.objects.get(code=user_data.get("code"))
        if user.code != code:
            return Response({"message": "wrong code" }, status=status.HTTP_404_NOT_FOUND)
        user_obj=CustomUser.objects.get(email=email)
        user_obj.is_active = True
        user_obj.save()
        return Response(data={"message": "go to login", f"{user_obj.username} is_active": user_obj.is_active}, status=status.HTTP_200_OK)



