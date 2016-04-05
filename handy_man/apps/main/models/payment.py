from django.db import models

from .job import Job
from .account_details import AccountDetails

from ..constants import PENDING


class Payment(models.Model):

    '''
    The payment model maintains a records of all the payments
    '''

    job = models.OneToOneField(Job)

    account_details = models.ForeignKey(AccountDetails, null=True)

    payment_status = models.CharField(
        verbose_name='Payment Status',
        max_length=10,
        default=PENDING,
    )

    amount = models.DecimalField(
        verbose_name='Amount in Pula',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    class Meta:
        app_label = 'main'
