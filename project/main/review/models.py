from operator import mod
from re import T
from unicodedata import name
from django.db import models
from user.models import CustomUser
# Create your models here.
class locations(models.Model):
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=300)
    picture = models.ImageField(upload_to='media/profiles/', default='profiles/default.png')
    long=models.DecimalField(max_digits=9, decimal_places=6)
    latt=models.DecimalField(max_digits=9, decimal_places=6)
    no_of_likes=models.DecimalField(max_digits=2,decimal_places=1, default=0.0)
    def __str__(self):
        return str(self.id)

class review(models.Model):
    title=models.CharField(max_length=300)
    id=models.BigAutoField(unique=True, primary_key=True)
    text = models.TextField()
    picture = models.ImageField(upload_to='media/profiles/', default='profiles/default.png')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    location=models.ForeignKey(locations,on_delete=models.CASCADE)
    date_created=models.DateTimeField(auto_now_add=True)
    liked_by=models.ManyToManyField(CustomUser,related_name="liked_by")
    def __str__(self):
        return str(self.id)

class Comment(models.Model):
    place = models.ForeignKey(review, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment_text = models.TextField(default='user comment')

    def __str__(self):
        return '"' + str(self.author)+ '"' + '`s Comment On ' + '<<' + str(self.place) + ">>"

