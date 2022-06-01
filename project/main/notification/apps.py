from django.apps import AppConfig
from django.db.models.signals import post_save

class NotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notification'
    def ready(self):
        # Implicitly connect a signal handlers decorated with @receiver.
        from . import signals
        # Explicitly connect a signal handler.
        post_save.connect(signals.send_notif,dispatch_uid="my_unique_identifier")