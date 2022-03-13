from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
path('register', views.RegisterView.as_view(), name="register"),
]