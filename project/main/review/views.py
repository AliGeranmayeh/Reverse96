
from functools import partial
from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import review_serializer, location_serializer,CommentSerializer,PollSerializer
from rest_framework import viewsets
from fluent_comments.models import FluentComment
from .models import Poll
from django.contrib.contenttypes.models import ContentType
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


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def retrieve(self, request, pk=None):
        poll = self.get_object(pk)
        serializer = self.serializer_class(poll,context={'request': request})
        return Response(serializer.data)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = FluentComment.objects.all()
    serializer_class = CommentSerializer
    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data = self.request.data
            comment = data['comment']
            poll = data['Poll']
            if 'parent' in data:
                parent = data['parent']
            else:
                parent = None
            submit_date = datetime.now()
            content = ContentType.objects.get(model="Poll").pk
            comment = FluentComment.objects.create(object_pk=poll, comment=comment, submit_date=submit_date, content_type_id=content,user_id = self.request.user.id,     site_id=settings.SITE_ID, parent_id=parent)
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)