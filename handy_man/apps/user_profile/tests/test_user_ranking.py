from django.test import TestCase

from .factories import UserProfileFactory
from ..models import UserProfile
from .factories import ProfessionFactory

from star_ratings.models import Rating
# from .profession_factory import ProfessionFactory


class TestUserRanking(TestCase):

    def setUp(self):
        self.profession = ProfessionFactory()
        self.artisan1 = UserProfileFactory(account_type='artisan', profession=self.profession)
        self.artisan2 = UserProfileFactory(account_type='artisan', profession=self.profession)
        self.artisan3 = UserProfileFactory(account_type='artisan', profession=self.profession)
        self.artisan4 = UserProfileFactory(account_type='artisan', profession=self.profession)
        self.artisan5 = UserProfileFactory(account_type='artisan', profession=self.profession)
        self.artisan6 = UserProfileFactory(account_type='artisan', profession=self.profession)
        self.customer1 = UserProfileFactory(account_type='customer', profession=None)
        self.customer2 = UserProfileFactory(account_type='customer', profession=None)
        self.customer3 = UserProfileFactory(account_type='customer', profession=None)

    def test_rating(self):
        # Avg. rating: 2.5
        Rating.objects.rate(self.artisan1, 4, self.customer1, '127.0.0.1')
        Rating.objects.rate(self.artisan1, 1, self.customer2, '127.0.0.1')

        # Avg. rating: 2
        Rating.objects.rate(self.artisan2, 1, self.customer2, '127.0.0.1')
        Rating.objects.rate(self.artisan2, 3, self.customer1, '127.0.0.1')

        artisans = UserProfile.objects.filter(ratings__isnull=False).order_by('ratings__average')
        self.assertEqual(artisans[0].pk, self.artisan2.pk)
        self.assertEqual(artisans[1].pk, self.artisan1.pk)
