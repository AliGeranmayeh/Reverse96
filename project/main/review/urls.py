from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('review', views.user_review.as_view(), name="user_review"),
    path('get_location', views.get_location_api.as_view(), name="add_location_api"),
    path('add_location', views.add_location_api.as_view(), name="get_location_api"),
]