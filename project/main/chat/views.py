from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from .models import Chat, Contact, Message
from django.db.models import Q

User = get_user_model()


def get_last_10_messages(chatId, Mid):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-timestamp').all()#[:Mid]


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)