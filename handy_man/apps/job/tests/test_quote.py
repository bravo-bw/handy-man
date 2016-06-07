from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import models

from handy_man.apps.user_profile.tests.factories import UserProfileFactory, ProfessionFactory

from ..models import Quote
from ..tests.factories import JobFactory, QuoteFactory, JobTypeFactory


class TestQuote(TestCase):

    def setUp(self):
        self.carpenter = ProfessionFactory(code='CP', profession_type='carpenter')
        self.plumber = ProfessionFactory(code='PL', profession_type='plumber')
        self.elec = ProfessionFactory(code='EL', profession_type='electrician')
        self.brick = ProfessionFactory(code='BL', profession_type='brick_layer')

        self.plumbing = JobTypeFactory(code='PL', name='plumbing', rate_per_hour=100.00)
        self.ectrical = JobTypeFactory(code='EL', name='electrical', rate_per_hour=250.00)

    def test_job_has_quote(self):
        job = JobFactory(job_type=self.plumbing)
        artisan1 = UserProfileFactory(profession=self.plumber)
        self.assertFalse(job.has_quote)
        quote = QuoteFactory(job=job, artisan=artisan1)
        self.assertTrue(job.has_quote)

    def test_allow_add_quote(self):
        job = JobFactory(job_type=self.plumbing)
        artisan1 = UserProfileFactory(profession=self.plumber)
        # No existing Quote
        self.assertTrue(job.allow_add_quote)
        quote1 = QuoteFactory(job=job, artisan=artisan1)
        # Pending action quote.
        self.assertFalse(job.allow_add_quote)
        quote1.accepted = False
        quote1.save()
        # Only existing quote rejected
        self.assertTrue(job.allow_add_quote)
        quote1.accepted = True
        quote1.save()
        # Quote accepted.
        self.assertFalse(job.allow_add_quote)

    def test_not_artisan_creating_quote(self):
        job = JobFactory(job_type=self.plumbing)
        non_artisan = UserProfileFactory(profession=None)
        with self.assertRaises(ValidationError):
            QuoteFactory(job=job, artisan=non_artisan)

    def test_wrong_profession_creating_quote(self):
        job = JobFactory(job_type=self.plumbing)
        non_artisan = UserProfileFactory(profession=self.elec)
        with self.assertRaises(ValidationError):
            QuoteFactory(job=job, artisan=non_artisan)

    def test_customer_accept_quote(self):
        job = JobFactory(job_type=self.plumbing)
        artisan1 = UserProfileFactory(profession=self.plumber)
        artisan2 = UserProfileFactory(profession=self.plumber)
        quote1 = QuoteFactory(job=job, artisan=artisan1)
        quote2 = QuoteFactory(job=job, artisan=artisan2)
        quote1.accepted = True
        quote1.save()
        self.assertFalse(Quote.objects.get(artisan=artisan2).accepted)
        self.assertIsNotNone(Quote.objects.get(artisan=artisan2).accepted)

    def test_customer_cancell_quote(self):
        job = JobFactory(job_type=self.plumbing)
        artisan1 = UserProfileFactory(profession=self.plumber)
        artisan2 = UserProfileFactory(profession=self.plumber)
        quote1 = QuoteFactory(job=job, artisan=artisan1)
        quote2 = QuoteFactory(job=job, artisan=artisan2)
        quote1.accepted = True
        quote1.save()
        quote1.accepted = None
        quote1.save()
        self.assertIsNone(Quote.objects.get(artisan=artisan2).accepted)

    def test_artisan_requoting_job(self):
        job = JobFactory(job_type=self.plumbing)
        artisan1 = UserProfileFactory(profession=self.plumber)
        quote1 = QuoteFactory(job=job, artisan=artisan1, amount=300)
        quote2 = QuoteFactory(job=job, artisan=artisan1, amount=500)
        self.assertTrue(Quote.objects.get(pk=quote1.pk).closed_requoted)

