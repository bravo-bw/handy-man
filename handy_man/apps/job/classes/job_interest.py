from handy_man.apps.job.models.job import Job


class JobInterest(object):

    def __init__(self, job, user_profile):
        self.job = job
        self.user_profile = user_profile

    @property
    def validate_job_interest(self):
        has_logged_interest = True if self.user_profile in self.job.artisan_interested.all() else False
        if self.job.status in ['assigned', 'completed'] or has_logged_interest:
            return False
        return True

    def add_job_interest(self):
        if self.job and self.validate_job_interest:
            job = self.job
            job.artisans_interested.add(self.user_profile)
            job.save()
            return True
        return False

    def cancel_job_interests(self):
        if self.job:
            job = self.job
            job.artisans_interested.remove(self.user_profile)
            job.save()
            return True
        return False

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

    @property
    def artisan_qualifications(self):
        artisan_qualifications = []
        return artisan_qualifications

    def job_qualification(self, job):
        job_qualification = []
        return job_qualification

    @property
    def artisan_jobs(self):
        """ returns a list of jobs artisan qualifies for."""
        artisan_jobs = []
        for job in self.all_new_jobs:
            for qualification in self.artisan_qualifications:
                if qualification in self.job_qualification(job):
                    artisan_jobs.append(job)
                    break
        return artisan_jobs
