from django.contrib import admin
from django.urls import path,re_path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name="register"),
    path('login', views.LoginView.as_view(), name="login"),
    path('login/refresh', jwt_views.TokenRefreshView.as_view(), name="refresh-token"),
    path('email-activision',views.EmailActivisionView.as_view(), name="email-activision"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('public-profile/<slug:slug>', views.PublicProfileView.as_view(), name="public-profile"),
    path('get-user-detail', views.get_user_detail.as_view(), name="get-user-detail"),
    path('Edit-userProfile', views.UserEditProfileView.as_view(), name="Edit-uesrProfile"),
    path('send-follow-request', views.send_follow_request.as_view(), name="follow-uesr"),
    path('accept-follow-request',views.accept_follow_request.as_view(),name='accept_follow_request'),
    path('unfollow-user',views.UnFollowUser.as_view(),name='unfollow_user'),
    path('remove-follower',views.RemoveFollower.as_view(),name='remove_follower'),
    path('change_password', views.ChangePasswordView.as_view(), name="change_password"),
]