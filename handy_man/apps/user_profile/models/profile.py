import hashlib
from datetime import datetime
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from ...main.choices import GENDER


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    mobile = models.CharField(max_length=10)
    alter_contact = models.CharField(max_length=10, null=True, blank=True)
    email_validated = models.BooleanField(default=False)
    administrator_validated = models.BooleanField(default=False)
    avatar_image = models.ImageField(upload_to=settings.STATIC_ROOT + '/gfx/',
                                     default=settings.STATIC_ROOT + '/gfx/default_avatar_male.jpg',
                                     null=True,
                                     blank=True)
#     account = models.CharField(max_length=10)
#     company = models.ForeignKey(Company, null=True)

    gender = models.CharField(
        max_length=6,
        choices=GENDER,
        null=True,
        blank=True,
    )

    dob = models.DateField(
        verbose_name='Date of Birth',
        null=True,
        blank=True,
    )

    omang = models.CharField(
        verbose_name='Omang no',
        max_length=9,
        null=True,
        blank=True,
    )

    def formated_dob(self):
        return self.dob.isoformat()

    def file_name(self):
        # Last element in the list is the file name
        return self.avatar_image.name.split('/')[-1:][0]

    def __unicode__(self):
        return '{} {} ({}), {}, {}'.format(self.user.first_name, self.user.last_name, self.user.username,
                                           self.user.email, 'location')

    class Meta:
        app_label = 'user_profile'

# User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
