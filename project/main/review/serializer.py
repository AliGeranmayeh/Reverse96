from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import places


class review_serializer(serializers.ModelSerializer):
    class Meta:
        model = places
        fields = ['id', 'name', 'user', 'address', 'picture']

