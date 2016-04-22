from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from handy_man.apps.main.constants import NEW
from handy_man.apps.main.choices import JOB_STATUS, JOB_TYPE
from handy_man.apps.geo_location.models import ItemGeolocationMixin
from handy_man.apps.user_profile.models import UserProfile


class Job(ItemGeolocationMixin):

    """
    This model describes the job and its details.
         1. Job Posting
         2. Job Allocation
         3. Job Quatation
         4. Job Payment
         5. Job Report
    """

    posted_by = models.ForeignKey(UserProfile, related_name='profile_sumbittor')

    allocated_to = models.ForeignKey(UserProfile, related_name='allocated', null=True, blank=True)

    identifier = models.AutoField(
        primary_key=True,
        verbose_name='Job Identifier',
        max_length=36,
        unique=True,
        editable=False
    )

    status = models.CharField(
        verbose_name='Job Status',
        max_length=50,
        default=NEW,
        choices=JOB_STATUS,
        editable=False
    )

    job_type = models.CharField(
        verbose_name='Job Type',
        max_length=25,
        choices=JOB_TYPE,
        null=True,
        blank=True
    )

    artisans_interested = models.ManyToManyField(
        UserProfile,
        null=True,
        blank=True
    )

    description = models.TextField(
        verbose_name='Detailed description of Job',
        max_length=250,
        null=True,
        blank=True
    )

    job_image_1 = models.FileField(upload_to=settings.STATIC_ROOT + '/gfx/',
                                  default=None,
                                  null=True,
                                  blank=True)
    job_image_2 = models.FileField(upload_to=settings.STATIC_ROOT + '/gfx/',
                                  default=None,
                                  null=True,
                                  blank=True)
    job_image_3 = models.FileField(upload_to=settings.STATIC_ROOT + '/gfx/',
                                  default=None,
                                  null=True,
                                  blank=True)

    class Meta:
        app_label = 'job'
