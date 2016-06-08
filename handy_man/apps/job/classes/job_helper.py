from handy_man.apps.user_profile.models.profile import UserProfile


class JobHelper(object):

    def __init__(self, job, job_type, estimated_job_closing_date, user):
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
