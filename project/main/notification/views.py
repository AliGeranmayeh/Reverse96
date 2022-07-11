from django.shortcuts import render
from .models import notification
from django.db.models import Q
# Create your views here.
def notif(T_user,user,content):
    notification.objects.create(to_user=T_user,from_user=user,content=content)

def get_notif(T_user,User):
    return notification.objects.filter(Q(to_user=T_user) | Q(from_user=User)).first()