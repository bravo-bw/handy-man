from django.db import models

from django.contrib.auth.models import User
from .job import Job


class JobRequest(models.Model):

    artisan = models.ForeignKey(verbose_name='Artisan', User)

    job = models.ForeignKey(verbose_name='Job', Job)

    class Meta:
        app_label = 'job'
