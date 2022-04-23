from urllib import request
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


from .models import locations, places


class review_serializer(serializers.ModelSerializer):
    class Meta:
        model = places
        fields = ['id', 'name', 'user', 'address', 'picture', 'date_created']
class location_serializer(serializers.ModelSerializer):
    class Meta:
        model = locations
        fields = ['id', 'long', 'latt']

