from django.db import models

from django.contrib.auth.models import User
from .job import Job


class JobRequest(models.Model):

    artisan = models.ForeignKey(User, verbose_name='Artisan')

    job = models.ForeignKey(Job, verbose_name='Job')

    class Meta:
        app_label = 'job'
