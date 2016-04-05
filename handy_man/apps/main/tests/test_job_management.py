from django.test.testcases import TestCase
from django.core.exceptions import ValidationError

from ..models import Job, Bid, Payment
from ..constants import (NEW, IN_PROGRESS, SHIPPER, INDIVIDUAL, UNDER_CONSIDERATION, ACCEPTED, REJECTED,
                         ASSIGNED, PENDING, ON_HOLD)
from .factories import UserProfileFactory, AccountFactory


class TestJobManagement(TestCase):

    def setUp(self):
        pass

    def test_individual_submit_job(self):
        individual = UserProfileFactory(account=INDIVIDUAL)
        job_options = {'weight': 300.00, }
        individual.create_job(job_options)
        self.assertEqual(Job.objects.filter(sumbittor__user__username=individual.user.username,
                                            job_status=NEW).count(), 1)
        exercutor = UserProfileFactory(account=SHIPPER)
        with self.assertRaises(ValidationError):
            exercutor.create_job(job_options)

    def test_directly_assign_job_to_shipper(self):
        individual = UserProfileFactory(account=INDIVIDUAL)
        job_options = {}
        individual.create_job(job_options)
        job = Job.objects.get(sumbittor__user__username=individual.user.username,
                              job_status=NEW)
        exercutor = UserProfileFactory(account=SHIPPER)
        job.assign_job(exercutor)
        self.assertEqual(Job.objects.filter(exercutor__user__username=exercutor.user.username,
                         job_status=ASSIGNED).count(), 1)
        with self.assertRaises(ValidationError):
            job.assign_job(individual)

    def test_multiple_shipper_bids_for_job(self):
        individual = UserProfileFactory(account=INDIVIDUAL)
        job_options = {}
        individual.create_job(job_options)
        job = Job.objects.get(sumbittor__user__username=individual.user.username,
                              job_status=NEW)
        exercutor1 = UserProfileFactory(account=SHIPPER)
        exercutor1.submit_bid(job, 200)
        self.assertEqual(Bid.objects.filter(job=job, bid_owner=exercutor1,
                                            bid_status=UNDER_CONSIDERATION, expired=False).count(), 1)
        exercutor2 = UserProfileFactory(account=SHIPPER)
        exercutor2.submit_bid(job, 200)
        self.assertEqual(Bid.objects.filter(job=job, bid_owner=exercutor2,
                                            bid_status=UNDER_CONSIDERATION, expired=False).count(), 1)

    def test_individual_accepts_bid(self):
        individual = UserProfileFactory(account=INDIVIDUAL)
        job_options = {}
        individual.create_job(job_options)
        job = Job.objects.get(sumbittor__user__username=individual.user.username,
                              job_status=NEW)
        exercutor1 = UserProfileFactory(account=SHIPPER)
        exercutor1.submit_bid(job, 200)
        exercutor2 = UserProfileFactory(account=SHIPPER)
        exercutor2.submit_bid(job, 200)
        bid = Bid.objects.get(job=job, bid_owner=exercutor2, bid_status=UNDER_CONSIDERATION, expired=False)
        individual.accept_bid(bid)
        self.assertEqual(Bid.objects.filter(job=job, bid_owner=exercutor2,
                                            bid_status=ACCEPTED, expired=False).count(), 1)

    def test_unaccepted_bid_automatically_rejected(self):
        individual = UserProfileFactory(account=INDIVIDUAL)
        job_options = {}
        individual.create_job(job_options)
        job = Job.objects.get(sumbittor__user__username=individual.user.username,
                              job_status=NEW)
        exercutor1 = UserProfileFactory(account=SHIPPER)
        exercutor1.submit_bid(job, 200)
        exercutor2 = UserProfileFactory(account=SHIPPER)
        exercutor2.submit_bid(job, 200)
        exercutor3 = UserProfileFactory(account=SHIPPER)
        exercutor3.submit_bid(job, 200)
        bid = Bid.objects.get(job=job, bid_owner=exercutor2, expired=False)
        individual.accept_bid(bid)
        self.assertEqual(Bid.objects.filter(job=job, bid_owner=exercutor2,
                                            bid_status=ACCEPTED, expired=False).count(), 1)
        for bid_item in Bid.objects.filter(job=job).exclude(bid_status=ACCEPTED):
            self.assertEqual(bid_item.bid_status, REJECTED)

    def test_accepted_bid_automatically_assigns_job(self):
        individual = UserProfileFactory(account=INDIVIDUAL)
        job_options = {}
        individual.create_job(job_options)
        job = Job.objects.get(sumbittor__user__username=individual.user.username,
                              job_status=NEW)
        exercutor1 = UserProfileFactory(account=SHIPPER)
        exercutor1.submit_bid(job, 200)
        exercutor2 = UserProfileFactory(account=SHIPPER)
        exercutor2.submit_bid(job, 200)
        bid = Bid.objects.get(job=job, bid_owner=exercutor2, expired=False)
        individual.accept_bid(bid)
        self.assertEqual(Bid.objects.get(job=job, bid_owner=exercutor2,
                                         bid_status=ACCEPTED, expired=False).job.job_status, ASSIGNED)

    def test_reject_job(self):
        individual = UserProfileFactory(account=INDIVIDUAL)
        job_options = {}
        individual.create_job(job_options)
        job = Job.objects.get(sumbittor__user__username=individual.user.username,
                              job_status=NEW)
        exercutor1 = UserProfileFactory(account=SHIPPER)
        job.assign_job(exercutor1)
        self.assertEqual(Job.objects.filter(sumbittor__user__username=individual.user.username,
                         job_status=ASSIGNED).count(), 1)
        exercutor1.reject_job(job)
        self.assertEqual(Job.objects.filter(sumbittor__user__username=individual.user.username,
                         job_status=NEW).count(), 1)

    def test_job_assigned_and_in_progress(self):
        individual = UserProfileFactory(account=INDIVIDUAL)
        job_options = {}
        individual.create_job(job_options)
        job = Job.objects.get(sumbittor__user__username=individual.user.username,
                              job_status=NEW)
        exercutor1 = UserProfileFactory(account=SHIPPER)
        job.assign_job(exercutor1)
        self.assertEqual(Job.objects.filter(sumbittor__user__username=individual.user.username,
                         job_status=ASSIGNED).count(), 1)
        exercutor1.accept_job(job)
        self.assertEqual(Job.objects.filter(sumbittor__user__username=individual.user.username,
                         job_status=ACCEPTED).count(), 1)
        exercutor1.make_job_in_progress(job)
        self.assertEqual(Job.objects.filter(sumbittor__user__username=individual.user.username,
                         job_status=IN_PROGRESS).count(), 1)

    def test_can_reject_assigned_job(self):
        individual = UserProfileFactory(account=INDIVIDUAL)
        job_options = {}
        individual.create_job(job_options)
        job = Job.objects.get(sumbittor__user__username=individual.user.username,
                              job_status=NEW)
        exercutor1 = UserProfileFactory(account=SHIPPER)
        job.assign_job(exercutor1)
        exercutor1.reject_job(job)
        self.assertEqual(Job.objects.filter(sumbittor__user__username=individual.user.username,
                         job_status=NEW).count(), 1)

    def test_can_only_reject_assigned_job(self):
        individual = UserProfileFactory(account=INDIVIDUAL)
        job_options = {}
        individual.create_job(job_options)
        job = Job.objects.get(sumbittor__user__username=individual.user.username,
                              job_status=NEW)
        exercutor1 = UserProfileFactory(account=SHIPPER)
        job.assign_job(exercutor1)
        exercutor1.accept_job(job)
        with self.assertRaises(ValidationError):
            exercutor1.reject_job(job)

    def test_accept_job_and_create_spawn_payment(self):
        individual = UserProfileFactory(account=INDIVIDUAL)
        job_options = {}
        individual.create_job(job_options)
        job = Job.objects.get(sumbittor__user__username=individual.user.username,
                              job_status=NEW)
        exercutor1 = UserProfileFactory(account=SHIPPER)
        job.assign_job(exercutor1)
        self.assertEqual(Job.objects.filter(sumbittor__user__username=individual.user.username,
                         job_status=ASSIGNED).count(), 1)
        exercutor1.accept_job(job)
        self.assertEqual(Job.objects.filter(sumbittor__user__username=individual.user.username,
                         job_status=ACCEPTED).count(), 1)
        job = Job.objects.get(sumbittor__user__username=individual.user.username,
                              job_status=ACCEPTED)
        self.assertEqual(Payment.objects.filter(job=job, payment_status=PENDING).count(), 1)

    def test_individual_makes_payment_on_hold(self):
        individual = UserProfileFactory(account=INDIVIDUAL)
        job_options = {}
        individual.create_job(job_options)
        job = Job.objects.get(sumbittor__user__username=individual.user.username,
                              job_status=NEW)
        exercutor1 = UserProfileFactory(account=SHIPPER)
        job.assign_job(exercutor1)
        self.assertEqual(Job.objects.filter(sumbittor__user__username=individual.user.username,
                         job_status=ASSIGNED).count(), 1)
        exercutor1.accept_job(job)
        self.assertEqual(Job.objects.filter(sumbittor__user__username=individual.user.username,
                         job_status=ACCEPTED).count(), 1)
        job = Job.objects.get(sumbittor__user__username=individual.user.username,
                              job_status=ACCEPTED)
        account = AccountFactory()
        job.initiate_payment(400, account.account_number)
        self.assertEqual(Payment.objects.filter(job=job, payment_status=ON_HOLD).count(), 1)



