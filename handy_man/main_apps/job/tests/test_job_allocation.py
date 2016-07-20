from django.test import TestCase

from handy_man.main_apps.job.classes import JobAllocation

from handy_man.main_apps.job.tests.factories.job_factory import JobFactory


class TestJobAllocation(TestCase):
    """
    1. Customer post a job
    2. Artisan logs an interest for the job
    3. Artisan generate a quotation
    4. Customer assigns a job
    """
    def setUp(self):
        self.job = JobFactory()
        self.user_profile = self.job.user_profile
        self.job_allocation = JobAllocation(job=self.job, user_profile=self.user_profile)

    def test_job_assign(self):
        self.assertTrue(self.job_allocation.assign_job)

    def test_cancel_assigned_job(self):
        self.assertTrue(self.job_allocation.assign_job)
        self.assertTrue(self.job_allocation.cancel_assigned_job)
