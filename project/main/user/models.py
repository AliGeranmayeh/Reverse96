from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class CustomUser(AbstractUser):
    name = models.CharField(max_length=300,null=True)
    username = models.CharField(max_length=300, unique=True)
    email = models.CharField(max_length=400, unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.IntegerField(unique=True,null=True)
    picture = models.ImageField(null=True, blank=True, upload_to='media/profiles/', default='profiles/default.png')
    address = models.TextField(null=True)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class EmailValidation(models.Model):
    code = models.IntegerField(unique=False)
    email = models.CharField(max_length=400, unique=True)
    def __str__(self):
        return self.email