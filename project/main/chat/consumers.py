from asyncio.windows_events import NULL
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from django.db.models.lookups import IsNull

from rest_framework.fields import NullBooleanField
from .models import Message, Chat, Contact
from .views import get_last_10_messages, get_reply_message, get_user_contact, get_current_chat,get_unseen_messages

User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = get_last_10_messages(data['chatId'])#,data['id'])
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        print(content)
        return self.send_message(content)

    def fetch_unseen_messages(self,data):
        user_contact = get_user_contact(data['from'])
        messages=get_unseen_messages(data['chatId'],user_contact)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        print(content)
        return    self.send_message(content)

    def new_message(self, data):
        user_contact = get_user_contact(data['from'])
        if 'reply' in data:
            message = Message.objects.create(
            contact=user_contact,
            reply=get_reply_message(data['chatId'],data['reply']),
            content=data['message'])
        else:
            message = Message.objects.create(
            contact=user_contact,
            content=data['message'])
        current_chat = get_current_chat(data['chatId'])
        current_chat.messages.add(message)
        current_chat.save()
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)


