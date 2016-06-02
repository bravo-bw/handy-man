from django.core.management.base import BaseCommand
from handy_man.apps.job.models import JobType
from handy_man.apps.user_profile.models import Profession


class Command(BaseCommand):

    args = 'number to create'
    help = 'Create job types on a fresh DB.'

    def handle(self, *args, **options):
        JobType.objects.get_or_create(code='CP', name='carpentry', rate_per_hour=50.00)
        JobType.objects.get_or_create(code='PL', name='plumbing', rate_per_hour=100.00)
        JobType.objects.get_or_create(code='EL', name='electrical', rate_per_hour=250.00)
        JobType.objects.get_or_create(code='BL', name='brick_laying', rate_per_hour=150.00)
        JobType.objects.get_or_create(code='TL', name='tile_laying', rate_per_hour=200.00)

        Profession.objects.get_or_create(profession_type='carpenter')
        Profession.objects.get_or_create(profession_type='plumber')
        Profession.objects.get_or_create(profession_type='electrician')
        Profession.objects.get_or_create(profession_type='brick_layer')
        Profession.objects.get_or_create(profession_type='tiler')
        Profession.objects.get_or_create(profession_type='roofer')