from datetime import timedelta, datetime

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import post_save
from notifications.signals import notify

from handy_man.main_apps.main.constants import NEW
from handy_man.main_apps.main.choices import JOB_STATUS
from handy_man.main_apps.geo_location.models import ItemGeolocationMixin
from handy_man.main_apps.user_profile.models import UserProfile
from handy_man.main_apps.job.managers import JobManager

from updown.fields import RatingField

from .job_type import JobType

estimated_closing_date = datetime.today().now() + timedelta(days=10)


def my_handler(sender, instance, created, **kwargs):
    g = Group.objects.get(name='artisan')
    notify.send(instance.posted_by.user, recipient=g, verb='new Job avaliable', action_object=instance.posted_by.user, description=instance.description)


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
        default=estimated_closing_date
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
        default=settings.MEDIA_ROOT + '/job_default1.png',
        null=True,
        blank=True
    )

    job_image_2 = models.ImageField(
        upload_to=settings.STATIC_ROOT + '/gfx/',
        default=settings.MEDIA_ROOT + '/job_default1.png',
        null=True,
        blank=True
    )
    job_image_3 = models.ImageField(
        upload_to=settings.STATIC_ROOT + '/gfx/',
        default=settings.MEDIA_ROOT + '/job_default1.png',
        null=True,
        blank=True
    )

    def job_image(self, image):
        if image:
            return '{}{}'.format(settings.STATIC_URL, image.name.split('/')[-1:][0])
        return ''

    @property
    def image_urls(self):
        return (self.job_image(self.job_image_1), self.job_image(self.job_image_2), self.job_image(self.job_image_3))

    @property
    def job_image_default(self):
        # Last element in the list is the file name
        if self.job_image(self.job_image) == '':
            return '{}{}'.format(settings.STATIC_URL, 'job_default1.png')
        return self.job_image(self.job_image_1)

    objects = JobManager()

    def __str__(self):
        return "{0}, {1}".format(self.job_type.name, self.job_type.code)

    @property
    def has_quote(self):
        Quote = apps.get_model('job', 'Quote')
        return Quote.objects.filter(job=self).exists()

    @property
    def fake_artisans_interested(self):
        return []

    class Meta:
        app_label = 'job'

post_save.connect(my_handler, sender=Job)