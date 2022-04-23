
from functools import partial
from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import review_serializer, location_serializer
from rest_framework.response import Response
from .models import places,locations
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.db.models import Q
from django.core.mail import send_mail
from rest_framework.generics import GenericAPIView

# Create your views here.
class user_review(APIView):
    permissions = [permissions.IsAuthenticated]
    def post(self,request):
        data=request.data
        # if("picture" in data):
        #     serializer_data={
        #         "address": data["address"],
        #         "name":data["name"],
        #         "user":request.user,
        #         "picture":data["picture"]
        #     }
        # else:
        #     serializer_data={
        #         "address": data["address"],
        #         "name":data["name"],
        #         "user":request.user
        #     }
        serializer = review_serializer(data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": serializer.data}, status=status.HTTP_201_CREATED)

class add_location_api(APIView):
    def post(self,request):
        data=request.data
        serializer = location_serializer(data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": serializer.data}, status=status.HTTP_201_CREATED)

class get_location_api(APIView):
    def get(self,request,pk=None):
        loc=locations.objects.filter(id=pk)
        serializer = location_serializer(loc, many=False)
        if(not loc):
            return Response({'message':"location does not exist"} ,status=status.HTTP_404_NOT_FOUND)
        else:
            existed_public_user_info = locations.objects.get(id=pk)
            serializer = location_serializer(existed_public_user_info, many=False)
            return Response({'message': serializer.data},status=status.HTTP_200_OK)