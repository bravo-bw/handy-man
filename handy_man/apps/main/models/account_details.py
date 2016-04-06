from django.db import models

from ..choices import PAYMENT_MODE, PAYMENT_STATUS, BANK, BANK_ACCOUNT_TYPE

from handy_man.apps.user_profile.models.profile import UserProfile


class AccountDetails(models.Model):

    '''
    Account details keeps record of the user's bank account details.
    '''

    user_profile = models.ForeignKey(UserProfile)

    account_number = models.CharField(
        verbose_name='Account Number',
        max_length=25,
        unique=True,
    )

    institution = models.CharField(
        verbose_name='Institution name',
        choices=BANK,
        max_length=25,
    )

    account_type = models.CharField(
        verbose_name='Account Type',
        max_length=25,
        choices=BANK_ACCOUNT_TYPE,
        null=True,
        blank=True,
    )

    payment_mode = models.CharField(
        verbose_name='Payment mode',
        max_length=25,
        choices=PAYMENT_MODE,
        null=True,
        blank=True,
    )

    class Meta:
        app_label = 'main'
