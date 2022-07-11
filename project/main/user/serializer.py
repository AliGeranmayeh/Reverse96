from rest_framework import serializers
from .models import CustomUser, EmailValidation, FollowRequest, UserFollowing
from django.utils.text import gettext_lazy
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.password_validation import validate_password


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(style={"input_type": "password"},
                                     required=True, allow_blank=False, allow_null=False)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'name', 'phone_number', 'address', 'is_active', 'picture','is_public']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'name', 'phone_number', 'address', 'is_active', 'picture','is_public']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class EmailActivisionSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField(required=True, allow_null=False)
    email = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    class Meta:
        model = EmailValidation
        fields = ['id', 'email', 'code']


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': gettext_lazy('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
class PictureSerializer(serializers.Serializer):
    picture=serializers.ImageField(max_length=None, use_url=True, allow_null=False, required=True)

class UserFollowerSerializer(serializers.ModelSerializer):
    picture=serializers.SerializerMethodField('picture_func')
    username=serializers.SerializerMethodField('username_func')
    name=serializers.SerializerMethodField('name_func')
    bio=serializers.SerializerMethodField('bio_func')
    def picture_func(self,instance):
        img={}
        img['picture']=instance.user_id.picture
        serializer=PictureSerializer(img)
        return serializer.data['picture']
    def username_func(self,instance):
        return instance.user_id.username
    def name_func(self,instance):
        return instance.user_id.name
    def bio_func(self,instance):
        return instance.user_id.bio
    class Meta:
         model=UserFollowing
         fields=('username','picture','name','bio')

class UserFollowingSerializer(serializers.ModelSerializer):
    picture=serializers.SerializerMethodField('picture_func')
    username=serializers.SerializerMethodField('username_func')
    name=serializers.SerializerMethodField('name_func')
    bio=serializers.SerializerMethodField('bio_func')
    def picture_func(self,instance):
        img={}
        img['picture']=instance.following_user_id.picture
        serializer=PictureSerializer(img)
        return serializer.data['picture']
    def username_func(self,instance):
        return instance.following_user_id.username
    def name_func(self,instance):
        return instance.following_user_id.name
    def bio_func(self,instance):
        return instance.following_user_id.bio
    class Meta:
         model=UserFollowing
         fields=('username','picture','name','bio')


class PublicProfileSerializer(serializers.ModelSerializer):
    followers=serializers.SerializerMethodField('adding_followers')
    followings=serializers.SerializerMethodField('adding_followings')
    mutuals=serializers.SerializerMethodField('adding_mutuals')
    def adding_followers(self,instance):
        serializer=UserFollowerSerializer(data=instance.followings.all(),many=True)
        serializer.is_valid()
        return serializer.data
    def adding_followings(self,instance):
        serializer=UserFollowingSerializer(data=instance.followers.all(),many=True)
        serializer.is_valid()
        return serializer.data
    def adding_mutuals(self,instance):
        follower_list=list(instance.followings.all())
        following_list=list(instance.followers.all())
        print(follower_list)
        print(following_list)
        mutual_list=[]
        for i in follower_list:
            for j in following_list:
                if i.user_id==j.following_user_id:
                    if j not in mutual_list:
                        mutual_list.append(j)
        serializer=UserFollowingSerializer(data=mutual_list,many=True)
        serializer.is_valid()
        return serializer.data


    class Meta:
        model = CustomUser
        fields = ['username', 'email',  'name', 'address','id',
                  'is_active', 'phone_number', 'picture','is_public','follow_state','followings',
                  'bio','description','liked','followers','mutuals']
        
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email',  'name', 'address',
                  'is_active', 'phone_number', 'picture','id','is_public']

class UserEditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email',  'name', 'address',
                  'is_active', 'phone_number', 'picture','is_public',
                  'bio','description']

        def validate_username(self, value):
            if CustomUser.objects.filter(username=value).exists():
                raise serializers.ValidationError("This username already exists!.")
            return value

        def update(self, validated_data):
            instance = self.Meta.model(**validated_data)
            return instance
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model=FollowRequest
        fields=['to_user','from_user','timestamp','is_active']
