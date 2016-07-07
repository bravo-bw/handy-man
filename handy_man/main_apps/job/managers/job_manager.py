from django.db import models
from django.db.models import Q
from handy_man.main_apps.main.choices import JOB_STATUS


class JobManager(models.Manager):

    def get_queryset(self):
        return super(JobManager, self).get_queryset()

    def latest_ten_jobs(self):
        return self.filter().order_by('-created')[:10]

    def available_jobs(self):
        return self.filter(status='New')
