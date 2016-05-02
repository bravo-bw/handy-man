from django.db import models

from handy_man.apps.main.choices import CURRENCY

from .job import Job


class Quote(models.Model):

    job = models.ForeignKey(Job, verbose_name='Job')

    currency = models.CharField(choices=CURRENCY,
                                max_length=10)

    estimate_hours = models.DecimalField(max_digits=5,
                                         decimal_places=2)

    rate_per_hour = models.DecimalField(max_digits=6,
                                        decimal_places=2)

    amount = models.DecimalField(max_digits=8,
                                 decimal_places=2)

    accepted = models.BooleanField(default=False)

    class Meta:
        app_label = 'job'
