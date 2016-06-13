from django.conf import settings
from django.apps import apps

from handy_man.apps.user_profile.models.profile import UserProfile

# from ..models import Quote


class JobHelper(object):

    def __init__(self, job=None, job_type=None, estimated_job_closing_date=None, user=None):
        self.job = job
        self.job_type = job_type
        self.job_closing_date = estimated_job_closing_date
        self.user = user

    @property
    def validate_job_change(self):
        if self.job.status in ['assigned', 'completed']:
            return False
        return True

    def save_job(self):
        if self.validate_job_change:
            if self.job_type:
                self.job.job_type = self.job_type
            if self.job_closing_date:
                self.job.estimated_closing_date = self.job_closing_date
            self.job.save()
            return True
        return False

    def add_job_interest(self):
        if self.validate_job_change:
            if not (self.user_profile in self.job.artisans_interested.all()):
                self.job.artisans_interested.add(self.user_profile)
                self.job.save()
                return True
        return False

    def notify_artisans(self):
        return False

    @property
    def user_profile(self):
        try:
            return UserProfile.objects.get(user=self.user)
        except UserProfile.DoesNotExist:
            return False

    def allow_add_quote(self, attempting_artisan):
        """Return False if i am an artisan that already has an open Quote for the Job,
        or if the open quote maximum number is reached for the job, else return True"""
        Quote = apps.get_model('job', 'Quote')
        if not attempting_artisan.profession:
            return False
        if (Quote.objects.filter(artisan=attempting_artisan, job=self.job, closed_requoted=False).exists() or
                Quote.objects.filter(job=self.job, closed_requoted=False).count() >= settings.MAX_QUOTE_NUMBER):
            return False
        return True

