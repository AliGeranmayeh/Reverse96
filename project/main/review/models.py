from operator import mod
from django.db import models
from user.models import CustomUser
# Create your models here.
class places(models.Model):
    name=models.CharField(max_length=300)
    id=models.BigAutoField(unique=True, primary_key=True)
    address = models.TextField()
    picture = models.ImageField(null=True, blank=True, upload_to='media/profiles/', default='profiles/default.png')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

#class location(models.Model):
    #long
    #latt
    