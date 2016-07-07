from handy_man.main_apps.job.models.job import Job
from handy_man.main_apps.main.constants import NEW


class JobInterest(object):

    def __init__(self, job=None, user_profile=None):
        self.job = job
        self.user_profile = user_profile

    @property
    def validate_job_interest(self):
        has_logged_interest = True if self.user_profile in self.job.artisan_interested.all() else False
        if self.job.status in ['assigned', 'completed'] or has_logged_interest:
            return False
        return True

    @property
    def jobs_with_job_interest_status(self):
        jobs_with_job_interest_status = []
        for job in self.all_new_jobs:
            self._job_identifier = job.identifier
            jobs_with_job_interest_status.append([job, self.job_interest_status(job)])
        return jobs_with_job_interest_status

    @property
    def latest_jobs(self):
        return Job.objects.latest_ten_jobs()

    @property
    def all_new_jobs(self):
        return Job.objects.available_jobs()

    def job_interest_status(self, job):
        try:
            return True if self.user_profile in job.artisans_interested.all() else False
        except AttributeError:
            return False

    def job_quatation_status(self, job):
        from handy_man.apps.job.models.quote import Quote
        try:
            return True if Quote.objects.filter(job=job, artisan=self.user_profile).exists() else False
        except AttributeError:
            return False

    def new_jobs(self):
        jobs = []
        for job in Job.objects.filter(status=NEW):
            jobs.append([job, self.job_quatation_status(job)])
        return jobs

