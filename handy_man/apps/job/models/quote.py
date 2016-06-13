from django.db import models

from handy_man.apps.main.choices import CURRENCY
from handy_man.apps.user_profile.models import UserProfile


from handy_man.apps.job.classes import QuoteHelper
from .job import Job


class Quote(models.Model):

    job = models.ForeignKey(Job, verbose_name='Job')

    artisan = models.ForeignKey(UserProfile, verbose_name='Job')

    currency = models.CharField(choices=CURRENCY,
                                max_length=10)

    estimate_hours = models.DecimalField(max_digits=5,
                                         decimal_places=2)

    rate_per_hour = models.DecimalField(max_digits=6,
                                        decimal_places=2)

    amount = models.DecimalField(max_digits=8,
                                 decimal_places=2)

    closed_requoted = models.BooleanField(default=False)

    accepted = models.NullBooleanField(default=None)

    def save(self, *args, **kwargs):
        self.rate_per_hour = self.amount / self.estimate_hours
        quote_helper = QuoteHelper(self)
        quote_helper.process()
        super(Quote, self).save(*args, **kwargs)

    class Meta:
        app_label = 'job'
#         unique_together = ('job', 'artisan', 'amount')
