import re
from django.db import models
# Create your models here.
class notification(models.Model):
    id=models.BigAutoField(primary_key=True)
    to_user=models.ForeignKey('user.CustomUser',related_name='notifee',on_delete=models.CASCADE)
    from_user=models.ForeignKey('user.CustomUser',related_name='notifer',on_delete=models.CASCADE)
    content=models.CharField(max_length=50,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    is_recieved=models.BooleanField(default=False)
    bazi=models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

