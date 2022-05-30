from functools import partial
from django.db.models import Max
from logging import raiseExceptions
from rest_framework.views import APIView
from .serializer import review_serializer, location_serializer,CommentSerializer, CommentCreationSerializer, location_review_serializer, review_serializer_username_inlcluded,Category_Serializer
from rest_framework.response import Response
from .models import review,locations, Comment
from user.models import CustomUser
from rest_framework import permissions, status
from django.db.models import Q
from django.core.mail import send_mail
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser

#from project.main.review import serializer

# Create your views here.
#locatin in map fram with child reviews
class get_map_location_view1(APIView):
    def post(self,request):
        coordinates=request.data['coordinates']
        map_locations=locations.objects.distinct().filter(Q(latt__range=[coordinates[0],coordinates[2]])
            & Q(long__range=[coordinates[1],coordinates[3]])).order_by('-no_of_likes')
        serializer=location_review_serializer(map_locations,many=True)
        return Response({'message': serializer.data},status=status.HTTP_200_OK)
#location within map frame without child reviews
class get_map_location_view(APIView):
    def post(self,request):
        coordinates=request.data['coordinates']
        map_locations=locations.objects.distinct().filter(Q(latt__range=[coordinates[0],coordinates[2]])
            & Q(long__range=[coordinates[1],coordinates[3]]))
        serializer=location_serializer(map_locations,many=True)
        return Response({'message': serializer.data},status=status.HTTP_200_OK)

def get_location_from_id(locationid):
    location=locations.objects.get(id=locationid)
    return location
#for home page and trends side bar
class get_reviews_api(APIView):
    permissions = [permissions.IsAuthenticated]
    def get(self,request,pk=None):
        if (pk=='1'):
            reviews=reviews_to_show(request.user)
            serializer=review_serializer_username_inlcluded(reviews,many=True)
            return Response({'message': serializer.data},status=status.HTTP_200_OK)
        elif (pk=='2'):
            reviews=review.objects.filter(is_public=True).annotate(max_weight=Max('liked_by')).order_by('-max_weight')[:10]
            serializer=review_serializer_username_inlcluded(reviews,many=True)
            return Response({'message': serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
def reviews_to_show(user,pk=None):
    if pk:
        reviews=review.objects.filter(location=pk).annotate(max_weight=Max('liked_by')).order_by('-max_weight')
    else:
        reviews=review.objects.all().order_by('-date_created')
    reviews_to_show=[]
    for i in list(reviews):
        if not i.is_public:
            for j in list(user.followings.all()):
                if i.user==j.following_user_id or i.user==user:
                    reviews_to_show.append(i)
        else:
            reviews_to_show.append(i)
    return reviews_to_show
#adding reviews of a location
class user_review(APIView):
    permissions = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def post(self,request):
        data=request.data
        _mutable = data._mutable
        data._mutable = True        # set to mutable
        data['user'] = request.user.id        # сhange the values you want
        if not request.user.is_public:
            data['is_public']=False
        data._mutable = _mutable        # set mutable flag back
        serializer = review_serializer(data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": serializer.data}, status=status.HTTP_201_CREATED)

class get_user_reviews(APIView):
    permissions = [permissions.IsAuthenticated]
    def get(self,requst,slug=None):
        user_revs=CustomUser.objects.get(username=slug)
        reviews=review.objects.filter(user=user_revs).order_by('-date_created')
        serializer=review_serializer(reviews,many=True)
        return Response({"message": serializer.data}, status=status.HTTP_200_OK)

class delete_user_reviews(APIView):
    permissions=[permissions.IsAuthenticated]
    def delete(self,request,pk):
        task = review.objects.get(id=pk)
        task.delete()
        return Response({"message": "item seuccesfuly deleted!"}, status=status.HTTP_200_OK)
class edit_user_reviews(APIView):
    permissions=[permissions.IsAuthenticated]   
    def post(self,request,pk=None):
        user_review=review.objects.get(id=pk)
        serializer=review_serializer(user_review,request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": serializer.data}, status=status.HTTP_205_RESET_CONTENT)

class add_location_api(APIView):
    permissions = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def post(self,request):
        data=request.data
        serializer = location_serializer(data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": serializer.data}, status=status.HTTP_201_CREATED)
#gettin a single location with id
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
# getting child reviews of a single location with its id           
class get_location_reviews(APIView):
    permissions = [permissions.IsAuthenticated]
    def get(self,request,pk=None):
        reviews=reviews_to_show(user=request.user,pk=pk)
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

    def post(self, request, pk=None):
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

    def post(self, request, pk=None):
        placees_info = review.objects.filter(id=pk)
        serializer = self.serializer_class(data=request.data)
        CommentSerializer(placees_info, many=False)
        serializer.is_valid()
        if not placees_info:
            return Response({'message': "Review does not exist"}, status=status.HTTP_404_NOT_FOUND)
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

#liking a riview
class RateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,pk=None):
        user=CustomUser.objects.get(username=request.user.username)
        liked_review=review.objects.get(id=pk)
        print(liked_review.liked_by.filter())
        if request.user in liked_review.liked_by.filter():
            liked_review.liked_by.remove(request.user)
            content = {'detail': 'successfully removed rate for place'}
            return Response(content, status=status.HTTP_201_CREATED)
        else:
            liked_review.liked_by.add(request.user)
            content = {'detail': 'successfully added rate for place'}
            return Response(content, status=status.HTTP_201_CREATED)


class Category(APIView):
    def post(self,request):
        coordinates=request.data['coordinates']
        serializer = Category_Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)        
        category= serializer.validated_data.get('place_category')

        if category:
            map_locations=locations.objects.distinct().filter(Q(latt__range=[coordinates[0],coordinates[2]])
                & Q(long__range=[coordinates[1],coordinates[3]]) & Q(place_category= category))
        else:
             map_locations=locations.objects.distinct().filter(Q(latt__range=[coordinates[0],coordinates[2]])
                & Q(long__range=[coordinates[1],coordinates[3]]))
        s = Category_Serializer(map_locations,many=True)
        return Response({'message': s.data},status=status.HTTP_200_OK)