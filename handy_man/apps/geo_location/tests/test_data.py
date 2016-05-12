from handy_man.apps.geo_location.models import Street, TownVillage, District
from handy_man.apps.user_profile.models import UserProfile
import factory
from django.contrib.auth.models import User


def create_districts(district_centers):
    """Create districts from a dictionary of district centers."""
    for key, value in district_centers.items():
        District.objects.create(district_name=key, center_latitude=value[0], center_longitude=value[1])


def create_town_village(towns_villages):
    """Create districts from a dictionary of district centers."""
    for key, value in towns_villages.items():
        district = District.objects.get(district_name=value[2])
        TownVillage.objects.create(town_village_name=key, center_latitude=value[0], center_longitude=value[1], district=district)


def create_streests(gaborone_streets, town_village):
    for key, value in gaborone_streets.items():
        Street.objects.create(street_name=key, center_latitude=value[0], center_longitude=value[1], town_village=town_village)

district_centers = {
    'north-west': [-19.330536, 23.588973], 'central': [-21.443605, 26.330152],
    'north-east': [-20.985286, 27.549635], 'gantsi': [-22.267728, 21.590500],
    'kgalagadi': [-24.725124, 21.820265], 'southren': [-24.804932, 24.709669],
    'kweneng': [-23.759405, 24.801545], 'south-east': [-24.947379, 25.759963],
    'kgatleng': [-24.198013, 26.354423]}

towns_villages = {
    'gaborone': [-24.604186, 25.939418, 'south-east'],
    'lobatse': [-25.200606, 25.688521, 'south-east'],
    'bobonong': [-21.972213, 28.421136, 'central'],
    'selibe-phikwe': [-22.007964, 27.838193, 'central']}

gaborone_streets = {'phase-2': [-24.644422, 25.896777],
                    'block-8': [-24.604342, 25.911437],
                    'old-naledi': [-24.686069, 25.899836],
                    'Extension-14': [-24.675040, 25.913407],
                    'bontleng': [-24.670117, 25.917330],
                    'g-west': [-24.659093, 25.895693]
                    }

# Create Botswana districts
create_districts(district_centers)


# Create towns for districts.
create_town_village(towns_villages)


# Create some of Gaborone streets
gaborone_town_village = TownVillage.objects.get(town_village_name='gaborone')
create_streests(gaborone_streets, gaborone_town_village)


# Create users.
def create_users():
    from datetime import date
    n = 0
    while n < 40:
        if n < 20:
            account_type = 'artisan'
            profession = 'carpenter'
        else:
            account_type = 'customer'
            profession = None
        user = User.objects.create(
            email='admin@gmail.com',
            first_name='user{0}'.format(n),
            last_name='user{0}'.format(n),
            username='user{0}'.format(n),
            password='user{0}'.format(n),
            is_active=True,
            is_staff=True)
        UserProfile.objects.create(
            user=user,
            mobile='7765769{0}'.format(n),
            email_validated=True,
            administrator_validated=True,
            gender='F',
            account_type=account_type,
            profession=profession,
            dob=date(1990, 12, 1),
        )
        n += 1
