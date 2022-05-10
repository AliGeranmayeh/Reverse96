from django.contrib import admin
from .models import review, locations, Comment

# Register your models here.
admin.site.register(review)
admin.site.register(Comment)
admin.site.register(locations)
