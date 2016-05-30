from django.test import TestCase

from ..classes import JobInterest
from handy_man.apps.job.tests.factories.job_factory import JobFactory


class TestJobInterest(TestCase):
    """
    1. Artisan shud view jobs in his area nd log in interest only for jobs that she/he qualifies for.
    2. Artisan shud view job status
    3.
    """
    def setUp(self):
        self.job = JobFactory()
        self.user_profile = self.job.user_profile
        self.job_interest = JobInterest(job=self.job, user_profile=self.user_profile)

    def test_add_job_interest(self):
        self.assertTrue(self.job_interest.add_job_interest())

    def test_cancel_job_interest(self):
        self.assertTrue(self.job_interest.add_job_interest())
        self.assertTrue(self.job_interest.cancel_job_interests())

    def test_validate_add_job_interest_one_on_one(self):
        """ 1. Artisan should not add more one job interest for a single job.
        """
        self.assertTrue(self.job_interest.add_job_interest())
        self.assertFalse(self.job_interest.add_job_interest())

    def test_validate_add_job_interest_closed_job(self):
        """
            2. Artisan should not able to add job interest for a closed job.
        """
        self.job.status = 'completed'
        self.job.save()

        self.job_interest = JobInterest(job=self.job, user_profile=self.user_profile)
        self.assertFalse(self.job_interest.add_job_interest())

    def test_validate_add_job_interest_assigned_job(self):
        """
            Artisan should not able to add job interest for assigned job
        """
        self.job.status = 'assigned'
        self.job.save()

        self.job_interest = JobInterest(job=self.job, user_profile=self.user_profile)
        self.assertFalse(self.job_interest.add_job_interest())
