from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from handy_man.apps.user_profile.tests.factories import UserProfileFactory, UserFactory
from ...constants import SHIPPER, INDIVIDUAL, NEW
from ...choices import CARGO_TYPE


class Command(BaseCommand):

    args = 'number to create'
    help = 'Create user_profile test data on a fresh DB.'

    def handle(self, *args, **options):
        user1 = User.objects.create_user('user1', 'user1@thebeatles.com', 'user1')
        user1.first_name = 'user1'
        user1.last_name = 'user1'
        user1.save()
        user2 = User.objects.create_user('user2', 'user2@thebeatles.com', 'user2')
        user2.first_name = 'user2'
        user2.last_name = 'user2'
        user2.save()
        user3 = User.objects.create_user('user3', 'user3@thebeatles.com', 'user3')
        user3.first_name = 'user3'
        user3.last_name = 'user3'
        user3.save()
        user4 = User.objects.create_user('user4', 'user4@thebeatles.com', 'user4')
        user4.first_name = 'user4'
        user4.last_name = 'user4'
        user4.save()
        individual1 = UserProfileFactory(user=user1)
        individual2 = UserProfileFactory(user=user2)
        shipper1 = UserProfileFactory(user=user3)
        shipper2 = UserProfileFactory(user=user4)
#         individual1.create_job({'job_status': NEW, 'starting_point': 'Lobatse', 'destination': 'Gaborone',
#                                 'cargo_type': CARGO_TYPE[0][0], 'description': 'Its just a job'})
#         individual1.create_job({'job_status': NEW, 'starting_point': 'Kanye', 'destination': 'Gaborone',
#                                 'cargo_type': CARGO_TYPE[1][0], 'description': 'Its just a job'})
#         individual2.create_job({'job_status': NEW, 'starting_point': 'Molepolole', 'destination': 'Gaborone',
#                                 'cargo_type': CARGO_TYPE[2][0], 'description': 'Its just a job'})
#         individual2.create_job({'job_status': NEW, 'starting_point': 'Lobatse', 'destination': 'Gaborone',
#                                 'cargo_type': CARGO_TYPE[3][0], 'description': 'Its just a job'})
