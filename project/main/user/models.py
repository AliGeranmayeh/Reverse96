from distutils.sysconfig import customize_compiler
import imp
import re
from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User



class CustomUser(AbstractUser):
    name = models.CharField(max_length=300)
    username = models.CharField(max_length=300, unique=True)
    email = models.CharField(max_length=400, unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11, unique=True)
    picture = models.ImageField(null=True, blank=True, upload_to='media/profiles/', default='profiles/default.png')
    address = models.TextField()
    is_active = models.BooleanField(default=False)
    is_public=models.BooleanField(default=True)
    liked=models.ManyToManyField('review.review', related_name='liked', blank=True )
    #followings=models.ForeignKey('self',blank=True,related_name='followings',on_delete=)
    #followers=models.ForeignKey('self',blank=True,related_name='followers')
    bio=models.CharField(max_length=100,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    follow_state=models.CharField(max_length=300, null=True,blank=True)
    def __str__(self):
        return self.username
    def __unicode__(self): 
        return self.username

class UserFollowing(models.Model):
    user_id = models.ForeignKey(CustomUser, related_name="followers", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(CustomUser, related_name="followings", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user_id.username

class EmailValidation(models.Model):
    code = models.IntegerField(unique=False)
    email = models.CharField(max_length=400, unique=True)
    def __str__(self):
        return self.email

class FollowRequest(models.Model):
    from_user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='request_from')
    to_user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='request_to')
    is_active=models.BooleanField(null=True,blank=True,default=True)
    timestamp=models.DateField(auto_now_add=True) 
    def __str__(self):
        return self.from_user.username