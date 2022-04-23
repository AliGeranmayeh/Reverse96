
from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import review_serializer, RegisterSerializer, EmailActivisionSerializer, RefreshTokenSerializer, PublicProfileSerializer
from rest_framework.response import Response
from .models import CustomUser,EmailValidation
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.generics import GenericAPIView

# Create your views here.
class user_review(APIView):
    permissions = [permissions.IsAuthenticated]
    def post(self,request):
        serializer = review_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": serializer.data}, status=status.HTTP_201_CREATED)
        
