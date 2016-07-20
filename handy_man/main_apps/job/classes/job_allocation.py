from handy_man.main_apps.main.choices import JOB_STATUS
from handy_man.main_apps.job.models.job import Job


class JobAllocation(object):
    """
        This class handles job requests for a particular job post. it will determine eligible artisan based on his or
        her rating, distance and availability.
        For example
        A customer will post a job A. if a system have 3 artisans, Artisan 1 is 2 km away from the location of the job
        and he has 4/5 rating, has submitted job request for Job A. Artisan 2 is 3 km away from the location of the job
        and he has 3/5 rating, has submitted job request for Job A.Artisan 3 is 4 km away from the location of the job
        and he has 2/5 rating, has submitted job request for Job A.
        Among the 3 artisans the system has to determine one qualified artisan for the job. In this case Artisan 1 is
        is qualified for the job A.
    """
    def __init__(self, job, user_profile):
        self.job = job
        self.user_profile = user_profile

    def order_by_rating(self, artisans):
        order_by_rating = artisans
        return order_by_rating

    def order_by_job_numbers(self, artisans):
        order_by_job_numbers = artisans
        i = 1
        for j in range(len(order_by_job_numbers)):
            if order_by_job_numbers[i][1] < order_by_job_numbers[j][1]:
                temp = order_by_job_numbers[i][1]
                order_by_job_numbers[i][1] = order_by_job_numbers[j][1]
                order_by_job_numbers[j][1] = temp
            i = i + 1
        return order_by_job_numbers

    def artisan_order(self):
        """ return [(with no jobs ), (with jobs)]"""
        with_current_jobs = []
        with_no_current_jobs = []
        artisans = self.job.artisans_interested.all()
        job_statuses = [status[i][0] for i, status in enumerate(JOB_STATUS[:2])]  # without completed
        for artisan in artisans:
            jobs = Job.objects.filter(allocated_to=artisan, status__in=job_statuses)
            if jobs:
                with_current_jobs.append([artisan, jobs.count()])
            else:
                with_no_current_jobs.append([artisan, 0])

        with_current_jobs = self.order_by_job_numbers(with_current_jobs)
        with_no_current_jobs = self.order_by_rating(with_no_current_jobs)
        interested_artisans = zip(with_no_current_jobs, with_current_jobs)
        return interested_artisans

    def assign_job(self):
        if self.job:
            job = self.job
            job.status = JOB_STATUS[2][0]
            job.allocated_to = self.user_profile
            job.save()
            return True
        return False

    def cancel_assigned_job(self):
        job = self.job
        is_cancelled = False
        if job:
            job.allocated_to = None
            job.status = job.status = JOB_STATUS[0][0]
            job.save()
            is_cancelled = True
        return is_cancelled

    @property
    def artisans(self):
        artisans = []
        job = self.job
        if job:
            for artisan in job.artisans_interested.all():
                temp = {}
                location = None
                try:
                    location = artisan.street.street_name if job.street.street_name else 'Botswana BW'
                except:
                    location = 'Botswana BW'
                temp.update({'artisan_id': artisan.id,
                             'username': artisan.user.username,
                             'full_name': "{} - {}".format(artisan.user.first_name, artisan.user.last_name),
                             'avatar': '/static/{}'.format(str(artisan.avatar_image).split('/')[-1]),
                             'job_identifier': job.identifier,
                             'latitude': artisan.latitude,
                             'longitude': artisan.longitude,
                             'selected': True if job.allocated_to else False,
                             'location': location})
                artisans.append(temp)
        return artisans

    @property
    def new_jobs_with_job_interest(self):
        new_jobs_with_job_interest = []
        for job in Job.objects.available_jobs():
            #if job.artisans_interested.all():
            new_jobs_with_job_interest.append(job)
        return new_jobs_with_job_interest

    def validate_job_assign(self):
        pass

    def qualified_artisan(self):
        pass

    def artisan_geo_location(self):
        pass

    def artisan_current_jobs(self):
        pass
