from django.db import IntegrityError

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from handy_man.main_apps.main.constants import ARTISAN, CUSTOMER, SME, HANDYMAN_ADMIN
from handy_man.main_apps.user_profile.models import UserProfile


def create_user_groups():
    try:
        artisans = Group(name=ARTISAN.title())
        artisans.save()
        print('Successfully Created ARTISAN Group.')
    except IntegrityError as e:
        print('ARTISAN Group already exists.')

    try:
        customer = Group(name=CUSTOMER.title())
        customer.save()
        print('Successfully Created CUSTOMER Group.')
    except IntegrityError as e:
        print('CUSTOMER Group already exists.')

    try:
        sme = Group(name=SME.title())
        sme.save()
        print('Successfully Created SME Group.')
    except IntegrityError as e:
        print('SME Group already exists.')

    try:
        handyman_admin = Group(name=HANDYMAN_ADMIN.title())
        handyman_admin.save()
        print('Successfully Created HANDYMAN_ADMIN Group.')
    except IntegrityError as e:
        print('HANDYMAN_ADMIN Group already exists.')

    artisan_group = Group.objects.get(name=ARTISAN)
    customer_group = Group.objects.get(name=CUSTOMER)
    sme_group = Group.objects.get(name=SME)
    handyman_group = Group.objects.get(name=HANDYMAN_ADMIN)

    try:
        user_profiles = UserProfile.objects.all()
    except Exception as e:
        print(e)

    added_to_group = 0
    try:
        print('Adding {} users to their groups.'.format(user_profiles.count()))
        for user in user_profiles:
            if user.account_type in CUSTOMER:
                user.user.groups.add(customer_group)
                added_to_group += 1
            elif user.account_type in ARTISAN:
                user.user.groups.add(artisan_group)
                added_to_group += 1
            elif user.user.account_type in SME:
                user.user.groups.add(sme_group)
                added_to_group += 1
            elif user.account_type in HANDYMAN_ADMIN:
                user.user.groups.add(handyman_group)
                added_to_group += 1
        print('Added {} users to groups.'.format(added_to_group))
    except IntegrityError as e:
        pass


class Command(BaseCommand):

    can_import_settings = True

    def handle(self, *args, **options):
        create_user_groups()
