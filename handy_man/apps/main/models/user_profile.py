import hashlib
from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from ..constants import INDIVIDUAL, SHIPPER, UNDER_CONSIDERATION, ACCEPTED, REJECTED, ASSIGNED, IN_PROGRESS, NEW
from ..choices import GENDER
from .company import Company


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    mobile = models.CharField(max_length=10)
    validated = models.BooleanField(default=False)
    account = models.CharField(max_length=10)
    company = models.ForeignKey(Company, null=True)

    gender = models.CharField(
        max_length=6,
        choices=GENDER,
        null=True,
        blank=True,
    )

    dob = models.DateField(
        verbose_name='Date of Birth',
        null=True,
        blank=True,
    )

    omang = models.CharField(
        verbose_name='Omang no',
        max_length=9,
        null=True,
        blank=True,
    )

    def create_job(self, options):
        Job = models.get_model('main', 'Job')
        if self.account == INDIVIDUAL:
            Job.objects.create(sumbittor=self, **options)
        else:
            raise ValidationError('Only INDIVIDUAL accounts can submit jobs. This is a "{}" account'.format(SHIPPER))

    def submit_bid(self, job, amount):
        Bid = models.get_model('main', 'Bid')
        if self.account == SHIPPER:
            Bid.objects.create(bid_owner=self, job=job, bidding_amount=amount, bid_status=UNDER_CONSIDERATION)
        else:
            raise ValidationError('Only SHIPPER accounts can submit bids against jobs. This is a "{}" account'.format(
                INDIVIDUAL))

    def accept_bid(self, bid):
        Bid = models.get_model('main', 'Bid')
        if self.account == INDIVIDUAL:
            bid.bid_status = ACCEPTED
            bid.save()
            job = bid.job
            job.assign_job(bid.bid_owner)
            for other_bid in Bid.objects.filter(job=bid.job).exclude(id=bid.id):
                other_bid.bid_status = REJECTED
                other_bid.save()
        else:
            raise ValidationError('Only INDIVIDUAL accounts can accept bids against jobs. This is a "{}" account'.format(
                SHIPPER))

    def reject_job(self, job):
        if job.job_status != ASSIGNED:
            raise ValidationError('Only a job with ASSIGNED status can be rejected. This is a "{}" job'.format(
                job.job_status))
        if self.account == SHIPPER:
            job.job_status = NEW
            job.exercutor = None
            job.save()
        else:
            raise ValidationError('Only SHIPPER accounts can reject jobs. This is a "{}" account'.format(INDIVIDUAL))

    def accept_job(self, job):
        if self.account == SHIPPER and job.job_status == ASSIGNED:
            job.job_status = ACCEPTED
            job.exercutor = self
            job.save()
        else:
            raise ValidationError(
                'Only SHIPPER accounts can accept jobs that are ASSIGNED. This is a "{}" account, job is {}.'.format(
                    INDIVIDUAL, job.job_status))

    def make_job_in_progress(self, job):
        if self.account == SHIPPER and job.job_status == ACCEPTED:
            job.job_status = IN_PROGRESS
            job.save()
        else:
            raise ValidationError(
                'Only SHIPPER accounts can make pro jobs that are ACCEPTED. This is a "{}" account, job is {}.'.format(
                    INDIVIDUAL, job.job_status))

    def gravatar_url(self):
        return "http://www.gravatar.com/avatar/%s?s=50" % hashlib.md5(self.user.email).hexdigest()

#     def __unicode__(self):
#         return (self.user.username,)

    class Meta:
        app_label = 'main'

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
