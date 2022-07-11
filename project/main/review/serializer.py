
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.fields import CurrentUserDefault
from .models import locations, review, Comment

class PictureSerializer(serializers.Serializer):
    picture=serializers.ImageField(max_length=None, use_url=True, allow_null=False, required=True)

class review_serializer(serializers.ModelSerializer):
    location_name=serializers.SerializerMethodField('get_name')
    location_picture=serializers.SerializerMethodField('get_picture')
    def get_name(self,instance):
        return instance.location.name
    def get_picture(self,instance):
        img={}
        img['picture']=instance.location.picture
        serializer=PictureSerializer(img)
        return serializer.data['picture']
    class Meta:
        model = review
        fields = ['id', 'title', 'user', 'text', 'picture', 'date_created','location','liked_by','is_public',
        'location_picture','location_name']

class user_review_serializer(serializers.ModelSerializer):
    location_name=serializers.SerializerMethodField('get_name')
    location_picture=serializers.SerializerMethodField('get_picture')
    comment_no=serializers.SerializerMethodField('get_comment_no')
    def get_name(self,instance):
        return instance.location.name
    def get_picture(self,instance):
        img={}
        img['picture']=instance.location.picture
        serializer=PictureSerializer(img)
        return serializer.data['picture']
    def get_comment_no(self,instance):
        return len(instance.comment_set.all())

    class Meta:
        model = review
        fields = ['id', 'title', 'user', 'text', 'picture', 'date_created','location','liked_by','is_public',
        'location_picture','location_name','comment_no']

class review_serializer_username_inlcluded(serializers.ModelSerializer):
    username=serializers.SerializerMethodField('username_function')
    def username_function(self,reviews):
        return reviews.user.username
    class Meta:
        model = review
        fields = ['id', 'title', 'user', 'text', 'picture', 'date_created','location','liked_by','username']


class location_serializer(serializers.ModelSerializer):
    no_of_reviews=serializers.SerializerMethodField('no_of_reviews_function')
    def no_of_reviews_function(self,locations):
        return len(locations.review_set.all())
    class Meta:
        model = locations
        fields = ('id','name','picture','long','latt','no_of_likes','no_of_reviews','place_category',)
    
class nameSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value

class location_review_serializer(serializers.ModelSerializer):
    reviews=serializers.SerializerMethodField('my_function')
    no_of_reviews=serializers.SerializerMethodField('no_of_reviews_function')
    def my_function(self,locations):
        serializer=review_serializer(data=locations.review_set.all(),many=True)
        serializer.is_valid()
        return serializer.data
    def no_of_reviews_function(self,locations):
        return len(locations.review_set.all())

    class Meta:
        model = locations
        fields = ('id','name','picture','long','latt','no_of_likes','reviews','no_of_reviews','place_category')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author', 'place', 'comment_text']



class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(
            value,
            context=self.context)
        return serializer.data

class CommentCreationSerializer(serializers.Serializer):
    comment_text = serializers.RegexField('')
    class Meta:
        model = Comment
        fields = ['author', 'place', 'comment_text']

def get_location_from_id(locationid):
    location=locations.objects.get(id=locationid)
    return location


class Category_Serializer(serializers.ModelSerializer):
    no_of_reviews=serializers.SerializerMethodField('no_of_reviews_function')
    place_category = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    long = serializers.DecimalField(max_digits=23, decimal_places=15, required=False)
    latt = serializers.DecimalField(max_digits=23, decimal_places=15, required=False)
    reviews = serializers.SerializerMethodField('my_function')

    def my_function(self, locations):
        serializer = review_serializer(data=locations.review_set.all(), many=True)
        serializer.is_valid()
        return serializer.data
    def no_of_reviews_function(self,locations):
        return len(locations.review_set.all())
    class Meta:
        model = locations
        fields = ('id', 'name', 'picture', 'long', 'latt', 'no_of_likes', 'no_of_reviews', 'place_category','reviews')