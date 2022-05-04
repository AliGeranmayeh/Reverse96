from urllib import request
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


from .models import locations, places


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


