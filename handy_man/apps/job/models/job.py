from django.db import models
from django.apps import apps
from django.contrib.auth.models import User
from django.conf import settings

from handy_man.apps.main.constants import NEW
from handy_man.apps.main.choices import JOB_STATUS, JOB_TYPE
from handy_man.apps.geo_location.models import ItemGeolocationMixin
from handy_man.apps.user_profile.models import UserProfile
from handy_man.apps.job.managers import JobManager


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

    def __str__(self):
        return self.job_type

    @property
    def has_quote(self):
        Quote = apps.get_model('job', 'Quote')
        return Quote.objects.filter(job=self).exists()

    @property
    def allow_add_quote(self):
        # TODO: implement this method to return True if a job had no Quote at all, all its Quotes are rejected or
        # there is no quote pending action.
        Quote = apps.get_model('job', 'Quote')
        if not Quote.objects.filter(job=self).exists():
            # Job has no quote at all.
            return True
        elif not Quote.objects.filter(job=self).exclude(accepted=False).exists():
            # All Quotes for a job rejected.
            return True
        elif Quote.objects.filter(job=self, accepted=True).exists():
            # A quote has been accepted.
            return False
        elif not Quote.objects.filter(job=self, accepted__isnull=True).exists():
            # No quote is pending actions. NOTE: there can ever be 1 quote pending action.
            return True
        return False

    @property
    def fake_artisans_interested(self):
        return []

    class Meta:
        app_label = 'job'
