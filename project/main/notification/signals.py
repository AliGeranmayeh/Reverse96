
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import notification


@receiver(post_save, sender=notification)
def send_notif(sender,instance,created, **kwargs):


    current_user = instance.to_user # Getting current user

    channel_layer = get_channel_layer()
    data = {
            "from":instance.from_user.username,
            "notif_id":instance.id,
            "notif":instance.content
            }
    group_name="notification_%s" % current_user.username
    async_to_sync(channel_layer.group_send)(
        group_name,  # Group Name, Should always be string
        {
            "type": "notification.message",   # Custom Function written in the consumers.py
            "message":{'messages':data,
                        'command':'post_connect'
                    }   
        },
    )