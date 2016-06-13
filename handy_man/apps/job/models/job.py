from django.db import models
from django.apps import apps
from django.contrib.auth.models import User
from django.conf import settings

from handy_man.apps.main.constants import NEW
from handy_man.apps.main.choices import JOB_STATUS, JOB_TYPE
from handy_man.apps.geo_location.models import ItemGeolocationMixin
from handy_man.apps.user_profile.models import UserProfile
from handy_man.apps.job.managers import JobManager

from updown.fields import RatingField

from .job_type import JobType


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

    rating = RatingField(can_change_vote=True)

    allocation_date = models.DateField(
        verbose_name='Allocation Date',
        null=True,
        blank=True,
    )

    completion_date = models.DateField(
        verbose_name='Completion Date',
        null=True,
        blank=True,
    )

    estimated_closing_date = models.DateField(
        verbose_name='Estimated Closing Date',
        null=True,
        blank=True,
    )

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

    job_type = models.ForeignKey(
        JobType,
        verbose_name='Job Type',
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

    job_image_1 = models.ImageField(
        upload_to=settings.STATIC_ROOT + '/gfx/',
        default=None,
        null=True,
        blank=True
    )

    job_image_2 = models.ImageField(
        upload_to=settings.STATIC_ROOT + '/gfx/',
        default=None,
        null=True,
        blank=True
    )
    job_image_3 = models.ImageField(
        upload_to=settings.STATIC_ROOT + '/gfx/',
        default=None,
        null=True,
        blank=True
    )

    objects = JobManager()

    def __str__(self):
        return (self.job_type.name,)

    @property
    def has_quote(self):
        Quote = apps.get_model('job', 'Quote')
        return Quote.objects.filter(job=self).exists()

    @property
    def fake_artisans_interested(self):
        return []

    class Meta:
        app_label = 'job'
