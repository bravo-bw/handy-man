from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel
from django.conf import settings

from handy_man.apps.main.constants import NEW
from handy_man.apps.main.choices import JOB_STATUS, JOB_TYPE
from handy_man.apps.geo_location.models import ItemGeolocationMixin
from handy_man.apps.user_profile.models import UserProfile
from handy_man.apps.job.managers import JobManager


class Job(ItemGeolocationMixin, TimeStampedModel):

    """
    This model describes the job and its details.
         1. Job Posting
         2. Job Allocation
         3. Job Quatation
         4. Job Payment
         5. Job Report
    """

    posted_by = models.OneToOneField(UserProfile, related_name='profile_sumbittor', editable=False)

    allocated_to = models.OneToOneField(UserProfile, related_name='allocated', editable=False)

    identifier = models.CharField(
        verbose_name='Job Identifier',
        default=None,
        max_length=36,
        unique=True,
        editable=False
    )

    category = models.CharField(
        verbose_name='Category',
        default=None,
        max_length=36,
        unique=True,
        editable=False
    )

    status = models.CharField(
        verbose_name='Job Status',
        max_length=10,
        default=NEW,
        choices=JOB_STATUS,
        editable=False
    )

    type = models.CharField(
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

    job_image_1 = models.FileField(
        upload_to=settings.STATIC_ROOT + '/gfx/',
        default=None,
        null=True,
        blank=True
    )

    job_image_2 = models.FileField(
        upload_to=settings.STATIC_ROOT + '/gfx/',
        default=None,
        null=True,
        blank=True
    )
    job_image_3 = models.FileField(
        upload_to=settings.STATIC_ROOT + '/gfx/',
        default=None,
        null=True,
        blank=True
    )

    objects = JobManager()

    class Meta:
        app_label = 'job'
