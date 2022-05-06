from django.contrib import admin
from .models import places, locations, Comment

# Register your models here.
admin.site.register(places)
admin.site.register(Comment)
admin.site.register(locations)