from ast import Delete
from functools import partial
from logging import raiseExceptions
from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import review_serializer, location_serializer,CommentSerializer, CommentCreationSerializer
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from .models import places,locations, Comment
from user.models import CustomUser
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.db.models import Q
from django.core.mail import send_mail
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.
class user_review(APIView):
    permissions = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def post(self,request):
        data=request.data
        data["user"]=request.user.id
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

class get_user_reviews(APIView):
    permissions = [permissions.IsAuthenticated]
    def get(self,requst):
        reviews=places.objects.filter(user=requst.user.id)
        serializer=review_serializer(reviews,many=True)
        return Response({"message": serializer.data}, status=status.HTTP_200_OK)

class delete_user_reviews(APIView):
    permissions=[permissions.IsAuthenticated]
    def delete(self,request,pk):
        task = places.objects.get(id=pk)
        task.delete()
        return Response({"message": "item seuccesfuly deleted!"}, status=status.HTTP_200_OK)
    

class add_location_api(APIView):
    permissions = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
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


#class PublicProfileView(APIView):
#   def get(self, request, pk=None):
#        public_user_info = CustomUser.objects.filter(username=pk)
#        serializer = PublicProfileSerializer(public_user_info, many=False)
#        if(not public_user_info):
#            return Response({'message':"user does not exist"} ,status=status.HTTP_404_NOT_FOUND)
#        else:
#           existed_public_user_info = CustomUser.objects.get(username=pk)
#           serializer = PublicProfileSerializer(existed_public_user_info, many=False)
#           return Response({'message': serializer.data},status=status.HTTP_200_OK)

class CommentViewAPI(APIView):
    serializer_class = CommentSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        placees_info = places.objects.filter(id=pk)
        CommentSerializer(placees_info, many=False)

        if not placees_info:
            return Response({'message': "place does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            comlist = [{'auth': com.author.username, 'text': com.comment_text} for com in
                       Comment.objects.filter(place=pk)]
            return Response({'message': comlist}, status=status.HTTP_201_CREATED)

class SubmitCommentAPI(APIView):
    serializer_class = CommentCreationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        placees_info = places.objects.filter(id=pk)
        serializer = self.serializer_class(data=request.data)
        CommentSerializer(placees_info, many=False)
        serializer.is_valid()
        if not placees_info:
            return Response({'message': "place does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            CommentInstance = Comment(place=places.objects.get(id=pk),
                                      author=CustomUser.objects.get(username=request.user),
                                      comment_text=serializer.validated_data.get("comment_text"))
            CommentInstance.save()
            return Response({'message': "comment submited "}, status=status.HTTP_201_CREATED)


class ViewRateView(APIView):

    def get(self, request, pk=None):
        place_info =get_object_or_404(places,id=pk)
        place=places.objects.get(id=pk)
        if not place_info:
            return Response({'message': "place does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            saved_list=place.liked_by
            print(saved_list)
            length_of_int = len(saved_list)
            if length_of_int != 0:

                content = {"Likes": length_of_int, "users": saved_list}
                return Response(content, status=status.HTTP_200_OK)
            else:
                content = {"likes": length_of_int}
                return Response(content, status=status.HTTP_204_NO_CONTENT)


# class RateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self,request,pk=None):
#         serializer = self.serializer_class(data=request.data)
#         print(request.data)
#         serializer.is_valid()
#         place_info = get_object_or_404(places, id=pk)
#         current_rate = serializer.validated_data.get("rate")
#         print(current_rate)
#         RateViewSerializer(place_info, many=False)
#         user = CustomUser.objects.get(username=request.user.username)
#         place = places.objects.get(id=pk)
#         #rate = Rate.objects.get(user=user, place=place)
#         #rate.rate += 1
#         new_rate = current_rate+1
#         rate = Rate(user=user, place=place, rate=1)
#         rate.save()
#         content = {'place': places.title, 'user': user.username,
#                    'detail': 'successfully added rate for place'}
#         return Response(content, status=status.HTTP_201_CREATED)

