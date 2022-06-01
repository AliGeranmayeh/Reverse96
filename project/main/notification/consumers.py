import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from user.models import CustomUser
from .models import notification

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'notification_%s' % self.room_name
        print(self.room_group_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        user=CustomUser.objects.get(username=self.room_name)
        notifs=notification.objects.filter(to_user=user)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'notification.message',
                'message': {'messages':self.messages_to_json(notifs),
                            'command': 'on_connect'
                            }   
            }
        )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if not(text_data_json['received_id'] is None):
            recieved_id=text_data_json['received_id']
            for i in recieved_id:
                notif=notification.objects.get(id=i)
                notif.delete()
        if not(text_data_json['message'] is None):
            message = text_data_json['message']
            print(message)
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'notification.message',
                    'message': message
                }
            )
    def messages_to_json(self, notifs):
        result = []
        for notif in notifs:
            result.append({
            "from":notif.from_user.username,
            "notif_id":notif.id,
            "notif":notif.content
            })
        return result   

    # Receive message from room group
    def notification_message(self, event):
        message = event['message']
        # Send message to WebSocket
        print(1)
        self.send(text_data=json.dumps({
            'message': message
        }))

