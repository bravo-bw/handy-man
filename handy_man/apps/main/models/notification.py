from django.db import models

from handy_man.apps.user_profile.models.user_profile import UserProfile


class Notification(models.Model):

    '''
    This model keeps record of all the notifications sent to all the users.
    '''

    owner = models.ForeignKey(UserProfile)

    sent = models.BooleanField(default=False)

    message_to = models.CharField(
        verbose_name='Sender: ',
        max_length=50,
    )

    subject = models.CharField(
        verbose_name='Subject',
        max_length=100,
    )

    message = models.TextField(
        verbose_name='Message: ',
        max_length=200,
    )

    class Meta:
        app_label = 'main'

