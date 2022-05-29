from django.contrib import admin
from .models import CustomUser,FollowRequest,UserFollowing

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(FollowRequest)
admin.site.register(UserFollowing)