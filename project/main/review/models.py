from operator import mod
from unicodedata import name
from django.db import models
from user.models import CustomUser
# Create your models here.
class places(models.Model):
    name=models.CharField(max_length=300)
    id=models.BigAutoField(unique=True, primary_key=True)
    address = models.TextField()
    picture = models.ImageField(null=True, blank=True, upload_to='media/profiles/', default='profiles/default.png')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    location=models.ForeignKey(location,on_delete=models.CASCADE)
    date_created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.id

class location(models.Model):
    id=models.BigAutoField(primary_key=True)
    long=models.DecimalField(max_digits=9, decimal_places=6)
    latt=models.DecimalField(max_digits=9, decimal_places=6)
    def __str__(self):
        return self.id    