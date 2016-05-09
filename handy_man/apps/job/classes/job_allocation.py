

class JobAllocationController(object):
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

    def job_requests(self):
        pass

    def qualified_artisan(self):
        pass

    def artisan_geo_location(self):
        pass

    def artisan_current_jobs(self):
        pass
