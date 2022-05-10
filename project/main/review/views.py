from ast import Delete
from functools import partial
from logging import raiseExceptions
from operator import truediv
from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import review_serializer, location_serializer,CommentSerializer, CommentCreationSerializer, location_review_serializer
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from .models import review,locations, Comment
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
class get_map_location_view1(APIView):
    def get(self,request):
        coordinates=request.data['coordinates']
        map_locations=locations.objects.distinct().filter(Q(latt__range=[coordinates[0],coordinates[2]])
            & Q(long__range=[coordinates[1],coordinates[3]])).order_by('-no_of_likes')
        serializer=location_review_serializer(map_locations,many=True)
        return Response({'message': serializer.data},status=status.HTTP_200_OK)

class get_map_location_view(APIView):
    def get(self,request):
        coordinates=request.data['coordinates']
        map_locations=locations.objects.distinct().filter(Q(latt__range=[coordinates[0],coordinates[2]])
            & Q(long__range=[coordinates[1],coordinates[3]])).order_by('-no_of_likes')
        serializer=location_serializer(map_locations,many=True)
        return Response({'message': serializer.data},status=status.HTTP_200_OK)

def get_location_from_id(locationid):
    location=locations.objects.get(id=locationid)
    return location

class get_reviews_api(APIView):
    def get(self,request,pk=None):
        if (pk=='1'):
            reviews=review.objects.all().order_by('-date_created')
            print(reviews)
            serializer=review_serializer(reviews,many=True)
            return Response({'message': serializer.data},status=status.HTTP_200_OK)
        elif (pk=='2'):
            reviews=review.objects.extra(select={'length':'length(liked_by)'}).order_by('length')[:10]
            print(reviews)
            serializer=review_serializer(reviews,many=True)
            return Response({'message': serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)







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
        reviews=review.objects.filter(user=requst.user.id)
        serializer=review_serializer(reviews,many=True)
        return Response({"message": serializer.data}, status=status.HTTP_200_OK)

class delete_user_reviews(APIView):
    permissions=[permissions.IsAuthenticated]
    def delete(self,request,pk):
        task = review.objects.get(id=pk)
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
            return Response({'message':"location does not exist"} ,status=status.HTTP_204_NO_CONTENT)
        else:
            existed_public_user_info = locations.objects.get(id=pk)
            serializer = location_serializer(existed_public_user_info, many=False)
            return Response({'message': serializer.data},status=status.HTTP_200_OK)
class get_location_reviews(APIView):
    def get(self,request,pk=None):
        reviews=review.objects.filter(location=pk)
        serializer=review_serializer(reviews, many=True)
        print(serializer.data)
        if not reviews:
            return Response({'message':"no reviews"} ,status=status.HTTP_204_NO_CONTENT)
        else:
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
        placees_info = review.objects.filter(id=pk)
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
        placees_info = review.objects.filter(id=pk)
        serializer = self.serializer_class(data=request.data)
        CommentSerializer(placees_info, many=False)
        serializer.is_valid()
        if not placees_info:
            return Response({'message': "place does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            CommentInstance = Comment(place=review.objects.get(id=pk),
                                      author=CustomUser.objects.get(username=request.user),
                                      comment_text=serializer.validated_data.get("comment_text"))
            CommentInstance.save()
            return Response({'message': "comment submited "}, status=status.HTTP_201_CREATED)


class ViewRateView(APIView):

    def get(self, request, pk=None):
        place_info =get_object_or_404(review,id=pk)
        place=review.objects.get(id=pk)
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
#         place_info = get_object_or_404(review, id=pk)
#         current_rate = serializer.validated_data.get("rate")
#         print(current_rate)
#         RateViewSerializer(place_info, many=False)
#         user = CustomUser.objects.get(username=request.user.username)
#         place = review.objects.get(id=pk)
#         #rate = Rate.objects.get(user=user, place=place)
#         #rate.rate += 1
#         new_rate = current_rate+1
#         rate = Rate(user=user, place=place, rate=1)
#         rate.save()
#         content = {'place': review.title, 'user': user.username,
#                    'detail': 'successfully added rate for place'}
#         return Response(content, status=status.HTTP_201_CREATED)

