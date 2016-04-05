import hashlib
from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from ...main.choices import GENDER


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    mobile = models.CharField(max_length=10)
    validated = models.BooleanField(default=False)
    photo = models.ImageField()
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

    omang = models.CharField(
        verbose_name='Omang no',
        max_length=9,
        null=True,
        blank=True,
    )

    def gravatar_url(self):
        return "http://www.gravatar.com/avatar/%s?s=50" % hashlib.md5(self.user.email).hexdigest()

#     def __unicode__(self):
#         return (self.user.username,)

    class Meta:
        app_label = 'user_profile'

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
