import hashlib
from datetime import datetime
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating

from ...main.choices import GENDER, ACCOUNT_TYPE, ARTISAN_PROFESSION
from handy_man.apps.geo_location.models import ItemGeolocationMixin


class UserProfile(ItemGeolocationMixin):
    user = models.OneToOneField(User)
    mobile = models.CharField(max_length=10)
    alter_contact = models.CharField(max_length=10, null=True, blank=True)
    email_validated = models.BooleanField(default=False)
    administrator_validated = models.BooleanField(default=False)
    ratings = GenericRelation(Rating, related_query_name='users')
    avatar_image = models.ImageField(upload_to=settings.MEDIA_ROOT,
                                     default=settings.MEDIA_ROOT + '/default_avatar_male.jpg',
                                     null=True,
                                     blank=True)
    document_1 = models.FileField(upload_to=settings.MEDIA_ROOT,
                                  default=None,
                                  null=True,
                                  blank=True)
    document_2 = models.FileField(upload_to=settings.MEDIA_ROOT,
                                  default=None,
                                  null=True,
                                  blank=True)
    document_3 = models.FileField(upload_to=settings.MEDIA_ROOT,
                                  default=None,
                                  null=True,
                                  blank=True)

    account_type = models.CharField(max_length=15,
                                    choices=ACCOUNT_TYPE,
                                    null=True,
                                    blank=True)

    profession = models.CharField(max_length=20,
                                  choices=ARTISAN_PROFESSION,
                                  null=True,
                                  blank=True)
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

    @property
    def get_user(self):
        return self.users

    def formated_dob(self):
        if self.dob:
            return self.dob.isoformat()
        return None

    @property
    def avatar_name(self):
        # Last element in the list is the file name
        if self.document(self.avatar_image) == '':
            return '{}{}'.format(settings.STATIC_URL, 'default_avatar_male.jpg')
        return self.document(self.avatar_image)

    @property
    def document_urls(self):
        return (self.document(self.document_1), self.document(self.document_2), self.document(self.document_3))

    def document(self, document):
        if document:
            return '{}{}'.format(settings.STATIC_URL, document.name.split('/')[-1:][0])
        return ''

    def __str__(self):
        return '{} {} ({}), {}, {}'.format(self.user.first_name, self.user.last_name, self.user.username,
                                           self.user.email, 'location')

    class Meta:
        app_label = 'user_profile'

# User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
