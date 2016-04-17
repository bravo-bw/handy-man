from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from handy_man.apps.user_profile.tests.factories import UserProfileFactory, UserFactory
from ...constants import SHIPPER, INDIVIDUAL, NEW
from ...choices import CARGO_TYPE


class Command(BaseCommand):

    args = 'number to create'
    help = 'Create user_profile test data on a fresh DB.'

    def handle(self, *args, **options):
        user1 = UserFactory(username='user1')
        user2 = UserFactory(username='user2')
        user3 = UserFactory(username='user3')
        user4 = UserFactory(username='user4')
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
