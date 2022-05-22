
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import tree
from user.models import CustomUser
User = get_user_model()


# class Contact(models.Model):
#     user = models.ForeignKey(CustomUser, related_name='friends', on_delete=models.CASCADE)
#     friends = models.ManyToManyField('self', blank=True)

#     def __str__(self):
#         return self.user.username


class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    contact = models.ForeignKey(
        CustomUser, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    reply=models.OneToOneField('self', null=True, blank=True, on_delete=models.CASCADE)
    flag=models.BooleanField(default=False)

    def __str__(self):
        return self.content


class Chat(models.Model):
    name=models.CharField(max_length=300, null=True, blank=True)
    participants = models.ManyToManyField(
        CustomUser, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return "{}".format(self.pk)