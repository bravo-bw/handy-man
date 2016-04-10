from django.test import TestCase
from django.db import models


class Artisan(models.Model):

    slug = models.SlugField(unique=True)

    first_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )


class TestJobAllocation(TestCase):

    def setUp(self):
        pass

    def test_interested_artisans(self):
        """ """
        pass

    def test_eligible_artisan(self):
        pass
