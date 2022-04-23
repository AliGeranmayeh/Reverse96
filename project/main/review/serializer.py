from urllib import request
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


from .models import places,location


class review_serializer(serializers.ModelSerializer):
    class Meta:
        model = places
        fields = ['id', 'name', 'user', 'address', 'picture', 'date_created']
class location_serializer(serializers.ModelSerializer):
    class Meta:
        model = location
        fields = ['id', 'long', 'latt']

