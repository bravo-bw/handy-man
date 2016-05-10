from handy_man.apps.job.models.job import Job


class JobInterest(object):

    def __init__(self, job, user_profile):
        self.job = job
        self.user_profile = user_profile

    def add_job_interest(self):
        if self.job:
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
        if self.job:
            for job in self.all_new_jobs:
                self._job_identifier = job.identifier
                jobs_with_job_interest_status.append([job, self.job_interest_status])
            return jobs_with_job_interest_status
        else:
            return []

    @property
    def latest_jobs(self):
        if self.job:
            return Job.objects.latest_ten_jobs()
        else:
            return []

    @property
    def all_new_jobs(self):
        return Job.objects.available_jobs()

    @property
    def job_interest_status(self):
        return True if self.user_profile in self.job.artisans_interested.all() else False

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
