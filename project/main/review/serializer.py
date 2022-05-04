from urllib import request
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from fluent_comments.models import FluentComment

from .models import locations, places,Poll


class review_serializer(serializers.ModelSerializer):
    class Meta:
        model = places
        fields = ['id', 'title', 'user', 'text', 'picture', 'date_created','location']
class location_serializer(serializers.ModelSerializer):
    class Meta:
        model = locations
        fields = ['id', 'long', 'latt']



class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(
            value,
            context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = FluentComment
        fields = ('comment', 'id', 'children',)


class PollSerializer(serializers.Serializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ('name', 'details', 'comments')

    def get_comments(self, obj):
        poll_comment = FluentComment.objects.filter(object_pk=obj.id, parent_id=None)
        serializer = CommentSerializer(poll_comment, many=True)
        return serializer.data