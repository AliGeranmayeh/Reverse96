from django.contrib import admin
from .models import places, locations, Comment,Rate

# Register your models here.
admin.site.register(places)
admin.site.register(Comment)
admin.site.register(locations)
admin.site.register(Rate)