from django.test import TestCase
from django.db import models

from ..tests.factories import JobFactory, QuoteFactory


class TestJobAllocation(TestCase):

    def setUp(self):
        pass

    def test_job_has_quote(self):
        job = JobFactory()
        self.assertFalse(job.has_quote)
        quote = QuoteFactory(job=job)
        self.assertTrue(job.has_quote)

    def test_allow_add_quote(self):
        job = JobFactory()
        # No existing Quote
        self.assertTrue(job.allow_add_quote)
        quote1 = QuoteFactory(job=job)
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

