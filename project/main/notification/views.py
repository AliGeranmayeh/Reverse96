from django.shortcuts import render
from .models import notification
# Create your views here.
def notif(T_user,user,content):
    notification.objects.create(to_user=T_user,from_user=user,content=content)