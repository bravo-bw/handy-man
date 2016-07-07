from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from handy_man.main_apps.job.tests.factories import JobFactory
from handy_man.main_apps.user_profile.models import Profession
from handy_man.main_apps.user_profile.tests.factories import UserProfileFactory


class Command(BaseCommand):

    args = 'number to create'
    help = 'Create user_profile test data on a fresh DB.'

    def handle(self, *args, **options):
        user1 = User.objects.create_user('user1', 'user1@thebeatles.com', 'user1')
        user1.first_name = 'user1'
        user1.last_name = 'user1'
        user1.account_type = 'customer'
        user1.save()
        user2 = User.objects.create_user('user2', 'user2@thebeatles.com', 'user2')
        user2.first_name = 'user2'
        user2.last_name = 'user2'
        user2.account_type = 'artisan'
        user2.save()
        user3 = User.objects.create_user('user3', 'user3@thebeatles.com', 'user3')
        user3.first_name = 'user3'
        user3.last_name = 'user3'
        user3.account_type = 'customer'
        user3.save()
        user4 = User.objects.create_user('user4', 'user4@thebeatles.com', 'user4')
        user4.first_name = 'user4'
        user4.last_name = 'user4'
        user4.account_type = 'artisan'
        user4.save()
        user1 = User.objects.get(first_name='user1')
        user2 = User.objects.get(first_name='user2')
        user3 = User.objects.get(first_name='user3')
        user4 = User.objects.get(first_name='user4')
        prof = Profession.objects.first()
        profile1 = UserProfileFactory(user=user1, profession=prof)
        profile2 = UserProfileFactory(user=user2, profession=prof)
        profile3 = UserProfileFactory(user=user3, profession=prof)
        profile4 = UserProfileFactory(user=user4, profession=prof)
        #job_type = JobType.objects.first()
        job1 = JobFactory(posted_by=profile2, allocated_to=profile1, status='new')
        job1 = JobFactory(posted_by=profile2, allocated_to=profile1, status='new')
        job3 = JobFactory(posted_by=profile3, allocated_to=profile1, status='completed')
