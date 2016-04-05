from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ..models import Notification


@receiver(post_save, weak=False, dispatch_uid="create_notification_on_post_save")
def create_notification_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        try:
            message_to, subject, message, owner = instance.email_notification_options()
            Notification.objects.create(message_to=message_to,
                                        subject=subject,
                                        message=message,
                                        owner=owner)
        except AttributeError:
            pass
