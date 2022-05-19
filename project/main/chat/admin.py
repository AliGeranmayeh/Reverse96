from operator import contains
from django.contrib import admin
from .models import  Message, Chat

# Register your models here.
#admin.site.register(Contact)
admin.site.register(Message)
admin.site.register(Chat)
