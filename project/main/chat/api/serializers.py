from rest_framework import serializers

from chat.models import Chat
from chat.views import get_user_contact


class ContactSerializer(serializers.StringRelatedField):
    name=serializers.CharField()
    def to_internal_value(self, value):
        return value

class nameSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value



class ChatSerializer(serializers.ModelSerializer):
    participants = ContactSerializer(many=True)
    class Meta:
        model = Chat
        fields = ('id', 'messages', 'participants', 'name','description','picture')
        read_only = ('id')

    def create(self, validated_data):
        print(validated_data)
        participants = validated_data.pop('participants')
        chat = Chat()
        chat.save()
        for username in participants:
            contact = get_user_contact(username)
            chat.participants.add(contact)
        chat.name=validated_data['name']
        if 'description' in validated_data:
            chat.description=validated_data['description']
        if 'picture' in validated_data:
            chat.picture=validated_data['picture']        
        chat.save()
        return chat


# do in python shell to see how to serialize data

# from chat.models import Chat
# from chat.api.serializers import ChatSerializer
# chat = Chat.objects.get(id=1)
# s = ChatSerializer(instance=chat)
# s
# s.data
