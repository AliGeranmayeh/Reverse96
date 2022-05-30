from dataclasses import is_dataclass
from functools import partial
from typing import Tuple
from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import LoginSerializer, RegisterSerializer, EmailActivisionSerializer, RefreshTokenSerializer, PublicProfileSerializer,UserEditProfileSerializer, ChangePasswordSerializer,UserDetailSerializer,FollowSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser,EmailValidation, FollowRequest, UserFollowing
from rest_framework import permissions, status, generics
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.core.mail import send_mail
from random import seed
from random import randint
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser

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
        print(user_code)
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
        #user_obj = CustomUser.objects.get(Q(username=username)|Q(email=username))
        if not user:
            return Response({"message": "invalid username or email"}, status=status.HTTP_404_NOT_FOUND)
        if not check_password(password, user.password):
            return Response({"message": "wrong password"}, status=status.HTTP_404_NOT_FOUND)
        if not user.is_active:
            return Response({"message": "validate your email"}, status=status.HTTP_403_FORBIDDEN)
        access_tk = str(AccessToken.for_user(user))
        refresh_tk = str(RefreshToken.for_user(user))
        return Response(data={"access": access_tk, "refresh": refresh_tk}, status=status.HTTP_200_OK)


class EmailActivisionView(APIView):
    def post(self,request):
        serializer= EmailActivisionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        code = serializer.validated_data.get("code")
        email = serializer.validated_data.get("email")
        user_info = CustomUser.objects.filter(Q(username=email)|Q(email=email)).first()
        if(user_info and user_info.is_active):
            return Response({"message": "your account is already activated"}, status=status.HTTP_208_ALREADY_REPORTED)
        else:
            if (not user_info):
                return Response({"message": "Invalid credentials"}, status=status.HTTP_404_NOT_FOUND)
                     
            user= EmailValidation.objects.get(email=email)
            if user.code != code:
                return Response({"message": "wrong code" }, status=status.HTTP_404_NOT_FOUND)
            user_info.is_active = True
            user_info.save()
            return Response(data={"message": "go to login", f"{user_info.username} is_active": user_info.is_active}, status=status.HTTP_200_OK)


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "logout process was successfull"},status=status.HTTP_204_NO_CONTENT)

class PublicProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, slug):
        public_user_info = CustomUser.objects.get(username=slug)
        serializer = PublicProfileSerializer(public_user_info, many=False)
        if(not public_user_info):
            return Response({'message':"user does not exist"} ,status=status.HTTP_404_NOT_FOUND)
        else:
            existed_public_user_info = CustomUser.objects.get(username=slug)
            following_state=FollowRequest.objects.distinct().filter(Q(to_user=public_user_info.id)&Q(from_user=request.user))
            if existed_public_user_info.followers.all().filter(user_id=request.user.id).exists():
                existed_public_user_info.follow_state="following"
            else:
                if following_state:
                    if following_state.is_active:
                        existed_public_user_info.follow_state="pending"
                    else:
                        existed_public_user_info.follow_state="declined"
                else:
                    existed_public_user_info.follow_state="follow"
            serializer = PublicProfileSerializer(existed_public_user_info, many=False)
            return Response({'message': serializer.data},status=status.HTTP_200_OK)

class get_user_detail(APIView):
    permissions = [permissions.IsAuthenticated]
    def get(self,request):
        user=request.user
        if (not user):
            return Response({'message':"user does not exist"} ,status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = PublicProfileSerializer(CustomUser.objects.get(username=user.username), many=False)
            return Response({'message': serializer.data},status=status.HTTP_200_OK)



class UserEditProfileView(APIView):
    permissions = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def patch(self, request):
        user = request.user
        serializer = UserEditProfileSerializer(user, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": serializer.data}, status=status.HTTP_205_RESET_CONTENT)

class send_follow_request(APIView):
        permissions = [permissions.IsAuthenticated]
        def post(self, request):
            user = request.user
            T_user=CustomUser.objects.get(username=request.data['to_user'])
            if FollowRequest.objects.filter(Q(from_user=user.id) & Q(to_user=T_user.id)).exists():
                F_requests=FollowRequest.objects.get(Q(from_user=user.id) & Q(to_user=T_user.id))
            print(user.followings.all())
            if user.followings.all().filter(following_user_id=T_user.id):
                return Response({"message": "alredy followed"}, status=status.HTTP_302_FOUND)
            if F_requests:
                if F_requests.is_active:
                    F_requests.delete()
                    return Response({"message": "friend request canceled"}, status=status.HTTP_410_GONE)
                else:
                    return Response({"message": "friend request is declined"}, status=status.HTTP_410_GONE)
            else:
                if T_user.is_public:
                    UserFollowing.objects.create(user_id=T_user,
                             following_user_id=user)
                    return Response({"message": "you have followed user"}, status=status.HTTP_201_CREATED)
                else:
                    serializer = FollowSerializer(data={'from_user':user.id,'to_user':T_user.id},partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response({"message": serializer.data}, status=status.HTTP_201_CREATED)

class accept_follow_request(APIView):
        permissions = [permissions.IsAuthenticated]
        def post(self, request):
            user = request.user
            F_user=CustomUser.objects.get(username=request.data['from_user'])
            if FollowRequest.objects.filter(Q(from_user=F_user) & Q(to_user=user)).exists():
                F_requests=FollowRequest.objects.get(Q(from_user=F_user) & Q(to_user=user))
            else:
                return Response({"message": "no new follow request"}, status=status.HTTP_204_NO_CONTENT)
            if F_requests.is_active==True:
                if request.data['accept']:
                    UserFollowing.objects.create(user_id=user,
                             following_user_id=F_user)
                    F_requests.delete()
                    return Response({"message": "follow request accepted"}, status=status.HTTP_202_ACCEPTED)
                else:
                    F_requests.is_active=False
                    F_requests.save()
                    return Response({"message": "follow request declined"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": " follow request is already declined"}, status=status.HTTP_204_NO_CONTENT)

class UnFollowUser(APIView):
        permissions = [permissions.IsAuthenticated]
        def post(self, request):
            user = request.user
            T_user=CustomUser.objects.get(username=request.data['user'])
            instance=UserFollowing.objects.filter(Q(user_id=user.id)&
                            Q( following_user_id=T_user.id))
            instance.delete()
            return Response({"message": "succesfully unfollowed"}, status=status.HTTP_205_RESET_CONTENT)
            
class RemoveFollower(APIView):
        permissions = [permissions.IsAuthenticated]
        def post(self, request):
            user = request.user
            T_user=CustomUser.objects.get(username=request.data['user'])
            instance=UserFollowing.objects.filter(Q(user_id=T_user.id)&
                            Q( following_user_id=user.id))
            instance.delete()
            return Response({"message": "succesfully removed follower"}, status=status.HTTP_205_RESET_CONTENT)


class ChangePasswordView(generics.UpdateAPIView):
    permissions = [permissions.IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(user, request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": serializer.data}, status=status.HTTP_205_RESET_CONTENT)
