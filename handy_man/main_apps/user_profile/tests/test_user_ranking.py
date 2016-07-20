from django.test import TestCase

from decimal import getcontext, Decimal

from handy_man.main_apps.user_profile.tests.factories import UserProfileFactory, UserFactory
from handy_man.main_apps.user_profile.tests.factories import ProfessionFactory
from handy_man.main_apps.job.tests.factories import JobFactory, JobTypeFactory, QuoteFactory
from handy_man.main_apps.user_profile.classes import UserRanking
from updown.models import SCORE_TYPES


class TestUserRanking(TestCase):

    def setUp(self):
        self.code = 'CP'
        self.profession = ProfessionFactory(profession_type='carpentry', code=self.code)
        self.customer1 = UserProfileFactory(account_type='customer', profession=None)
        self.job_type = JobTypeFactory(name='carpentry', code=self.code)
        self.job = JobFactory(posted_by=self.customer1, job_type=self.job_type)
        self.artisan1 = UserProfileFactory(account_type='artisan', profession=self.profession)
        self.artisan4 = UserProfileFactory(account_type='artisan', profession=self.profession)
        self.artisan2 = UserProfileFactory(account_type='artisan')
        self.customer2 = UserProfileFactory(account_type='customer', profession=None)
        self.customer3 = UserProfileFactory(account_type='customer', profession=None)
        self.customer4 = UserProfileFactory(account_type='customer', profession=None)
        self.customer5 = UserProfileFactory(account_type='customer', profession=None)
        self.artisan1_quote = QuoteFactory(
            job=self.job,
            artisan=self.artisan1,
            estimate_hours=2.0,
            rate_per_hour=100.00,
            amount=200.00)
        self.artisan3 = UserProfileFactory(account_type='artisan', profession=self.profession)

        #  New jobs
        self.completed_job1 = JobFactory(
            posted_by=self.customer1, job_type=self.job_type)
        self.completed_job2 = JobFactory(
            posted_by=self.customer1, job_type=self.job_type)
        self.completed_job3 = JobFactory(
            posted_by=self.customer1, job_type=self.job_type)

        # Job quotes
        self.artisan3_job1_quote = QuoteFactory(
            job=self.completed_job1, artisan=self.artisan3, estimate_hours=1.0, amount=100.00)
        self.artisan3_job2_quote = QuoteFactory(
            job=self.completed_job2, artisan=self.artisan3, estimate_hours=2.0, amount=100.00)
        self.artisan3_job3_quote = QuoteFactory(
            job=self.completed_job3, artisan=self.artisan3, estimate_hours=1.0, amount=100.00)

        #  Completed jobs
        self.completed_job1.allocated_to = self.artisan3
        self.completed_job1.status = 'completed'
        self.completed_job1.save()
        self.completed_job2.allocated_to = self.artisan3
        self.completed_job2.status = 'completed'
        self.completed_job2.save()
        self.completed_job3.allocated_to = self.artisan3
        self.completed_job3.status = 'completed'
        self.completed_job3.save()

        # First job rating
        self.completed_job1.rating.add(SCORE_TYPES['LIKE'], self.customer2.user, '192.168.1.22')
        self.completed_job1.rating.add(SCORE_TYPES['LIKE'], self.customer3.user, '192.168.1.23')
        self.completed_job1.rating.add(SCORE_TYPES['LIKE'], self.customer4.user, '192.168.1.24')
        self.completed_job1.rating.add(SCORE_TYPES['DISLIKE'], self.customer5.user, '192.168.1.21')
        self.user_ranking = UserRanking()

    def test_qualification_marks(self):
        """Test if qualification marks for an artisan who qualifies are calculated correctly."""
        expected_marks = Decimal(0.15)
        self.assertEqual(self.user_ranking.qualified_for_profession_marks(self.artisan1, self.job), expected_marks)

    def test_no_qualification_marks(self):
        """Test if someone who does not qualify get no marks."""
        self.assertEqual(self.user_ranking.qualified_for_profession_marks(self.artisan2, self.job), 0)

    def test_job_rate_marks(self):
        """Test calculate marks for a job quote."""
        # Set the precision.
        getcontext().prec = 2
        expected_value = Decimal(0.25) * Decimal(1)
        self.assertEqual(
            self.user_ranking.job_rate_marks(self.artisan1_quote.rate_per_hour, self.artisan1_quote.rate_per_hour),
            expected_value)

    def test_satisfaction_marks(self):
        """Test calculation for satifaction marks."""
        getcontext().prec = 2
        expected_marks = Decimal(0.00050) * Decimal(1)
        self.assertEqual(self.user_ranking.satisfaction_marks(self.artisan3), expected_marks)

    def test_user_jobs_completed_marks(self):
        """Test calculation for completed jobs."""
        getcontext().prec = 2
        expected_marks = Decimal(0.00060) * Decimal(1)
        self.assertEqual(self.user_ranking.user_jobs_completed_marks(self.artisan3), expected_marks)

    def test_user_current_jobs_marks(self):
        """Test calculation for current job for a user."""
        #  New jobs
        artisan4_job1 = JobFactory(
            posted_by=self.customer1, job_type=self.job_type)
        artisan4_job2 = JobFactory(
            posted_by=self.customer1, job_type=self.job_type)
        artisan4_job3 = JobFactory(
            posted_by=self.customer1, job_type=self.job_type)

        # Job quotes
        QuoteFactory(
            job=artisan4_job1, artisan=self.artisan4, estimate_hours=1.0, amount=100.00)
        QuoteFactory(
            job=artisan4_job2, artisan=self.artisan4, estimate_hours=2.0, amount=100.00)
        QuoteFactory(
            job=artisan4_job3, artisan=self.artisan4, estimate_hours=1.0, amount=100.00)

        #  Completed jobs
        artisan4_job1.allocated_to = self.artisan4
        artisan4_job1.status = 'in_progess'
        artisan4_job1.save()
        artisan4_job2.allocated_to = self.artisan4
        artisan4_job2.status = 'in_progess'
        artisan4_job2.save()
        artisan4_job3.allocated_to = self.artisan4
        artisan4_job3.status = 'in_progess'
        artisan4_job3.save()

        expected_marks = Decimal(0.015) * Decimal(1)
        self.assertEqual(self.user_ranking.user_current_jobs_marks(self.artisan4), expected_marks)

    def test(self):
        """Test ranking quotes."""
        rated_job = JobFactory(posted_by=self.customer1, job_type=self.job_type)

        # User factories
        user1 = UserFactory(first_name='mpho', last_name='thuto', username='mthuto')
        user2 = UserFactory(first_name='james', last_name='pual', username='jpual')
        user3 = UserFactory(first_name='precious', last_name='jane', username='pjane')
        user4 = UserFactory(first_name='jason', last_name='trade', username='jtrade')

        #  New Artisans
        artisan5 = UserProfileFactory(account_type='artisan', profession=self.profession, user=user1)
        artisan6 = UserProfileFactory(account_type='artisan', profession=self.profession, user=user2)
        artisan7 = UserProfileFactory(account_type='artisan', profession=self.profession, user=user3)
        artisan8 = UserProfileFactory(account_type='artisan', profession=self.profession, user=user4)
        # Job quotes
        q1 = QuoteFactory(
            job=rated_job, artisan=artisan5, estimate_hours=1.5, amount=500.00)
        q2 = QuoteFactory(
            job=rated_job, artisan=artisan6, estimate_hours=1.0, amount=10.00)
        q3 = QuoteFactory(
            job=rated_job, artisan=artisan7, estimate_hours=0.5, amount=100.00)
        q4 = QuoteFactory(
            job=rated_job, artisan=artisan8, estimate_hours=1.0, amount=100.00)
#         for quote in self.user_ranking.return_ranked_quotations(rated_job):
#             print(quote[0].artisan.user.first_name, "first name", quote[1], "marks rated")
        self.assertEqual(
            self.user_ranking.return_ranked_quotations(rated_job)
            [(q4, Decimal('0.400')), (q1, Decimal('0.150')), (q2, Decimal('0.150')), (q3, Decimal('0.150'))])
