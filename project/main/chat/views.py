from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from .models import Chat,  Message
from user.models import CustomUser
from django.db.models import Q

User = get_user_model()


def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('timestamp').all()#[:Mid]

def get_unseen_messages(chatId, Mfrom):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.filter(Q(flag=False) & ~Q(contact=Mfrom)).order_by('-timestamp')


def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(User, username=username)

def get_reply_message(chatId,Mid):
    chat = get_object_or_404(Chat, id=chatId)
    msg =chat.messages.get(id=Mid)
    return msg

def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)