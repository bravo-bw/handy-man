from django.db import models
from django_extensions.db.models import TimeStampedModel


class JobType(TimeStampedModel):

    code = models.CharField(
        max_length=5
    )

    name = models.CharField(
        max_length=15
    )

    rate_per_hour = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    def __str_(self):
        return self.name

    class Meta:
        app_label = 'job'
