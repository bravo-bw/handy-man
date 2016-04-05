import uuid
from django.db import models
from django.core.exceptions import ValidationError

from handy_man.apps.user_profile.models.user_profile import UserProfile
from .account_details import AccountDetails
from ..constants import NEW, INDIVIDUAL, SHIPPER, ASSIGNED, ON_HOLD, ACCEPTED, PENDING
from ..choices import JOB_STATUS, CARGO_TYPE


class Job(models.Model):

    """
    This model describes the job and its details.
    """

    sumbittor = models.ForeignKey(UserProfile, related_name='profile_sumbittor', editable=False)

    exercutor = models.ForeignKey(UserProfile, null=True, editable=False)

    job_identifier = models.CharField(
        verbose_name='Job Identifier',
        default=None,
        max_length=36,
        unique=True,
        editable=False
    )

    starting_point = models.CharField(
        verbose_name='Starting Point',
        max_length=10,
        null=True,
        blank=True
    )

    destination = models.CharField(
        verbose_name='destination',
        max_length=10,
        null=True,
        blank=True
    )

    job_status = models.CharField(
        verbose_name='Job Status',
        max_length=10,
        default=NEW,
        choices=JOB_STATUS,
        editable=False
    )

    weight = models.DecimalField(
        verbose_name='Weight of the Cargo',
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )

    insurance = models.CharField(
        verbose_name='Insurance',
        max_length=25,
        null=True,
        blank=True
    )

    cargo_type = models.CharField(
        verbose_name='Type of Cargo',
        max_length=25,
        choices=CARGO_TYPE,
        null=True,
        blank=True
    )

    description = models.TextField(
        verbose_name='Detailed description of Cargo',
        max_length=250,
        null=True,
        blank=True
    )

    start_lat = models.DecimalField(
        verbose_name=' start latitude',
        max_digits=10,
        null=True,
        blank=True,
        decimal_places=6)

    start_lon = models.DecimalField(
        verbose_name='start longitude',
        max_digits=10,
        null=True,
        blank=True,
        decimal_places=6)

    dest_lat = models.DecimalField(
        verbose_name='end latitude',
        max_digits=10,
        null=True,
        blank=True,
        decimal_places=6)

    dest_lon = models.DecimalField(
        verbose_name='end longitude',
        max_digits=10,
        null=True,
        blank=True,
        decimal_places=6)

    def assign_job(self, exercutor):
        if exercutor.account == SHIPPER:
            self.exercutor = exercutor
            self.job_status = ASSIGNED
            self.save()
        else:
            raise ValidationError('Only SHIPPER accounts can execute jobs. This is a "{}" account'.format(INDIVIDUAL))

    def initiate_payment(self, amount, account_number):
        Payment = models.get_model('main', 'Payment')
        account_details = AccountDetails.objects.get(account_number=account_number)
        payment = Payment.objects.get(job=self)
        payment.account_details = account_details
        payment.amount = amount
        payment.payment_status = ON_HOLD
        payment.save()

    def save(self, *args, **kwargs):
        Payment = models.get_model('main', 'Payment')
        if not self.id:
            self.job_identifier = str(uuid.uuid4())
        if self.job_status == ACCEPTED:
            try:
                Payment.objects.get(job=self)
            except Payment.DoesNotExist:
                Payment.objects.create(job=self, payment_status=PENDING)
        super(Job, self).save(*args, **kwargs)

    def email_notification_options(self):
        message_to = self.sumbittor.user.email
        subject = "Job '{}' has been update".format(self.job_identifier)
        message = "Job '{}' has been update".format(self.job_identifier)
        owner = self.sumbittor
        return (message_to, subject, message, owner)

    class Meta:
        app_label = 'main'
