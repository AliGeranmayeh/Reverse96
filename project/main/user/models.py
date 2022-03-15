from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class CustomUser(AbstractUser):
    name = models.CharField(max_length=300)
    username = models.CharField(max_length=300, unique=True)
    email = models.CharField(max_length=400, unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.IntegerField(unique=True)
    address = models.TextField()
    def __str__(self):
        return self.username

class EmailValidation(models.Model):
    code = models.CharField(max_length=4)
    email = models.CharField(max_length=400, unique=True)
    def __str__(self):
        return self.username