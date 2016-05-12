import factory
from django.contrib.auth.models import User

from handy_man.apps.user_profile.models import UserProfile
from .profession_factory import ProfessionFactory
from datetime import date


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = User

    email = 'admin@gmail.com'
    first_name = factory.Sequence(lambda n: 'user{0}'.format(n))
    last_name = factory.Sequence(lambda n: 'user'.format(n))
    username = factory.Sequence(lambda n: 'user{0}'.format(n))
#     password1 = '1'
#     password2 = '1'


class UserProfileFactory(factory.DjangoModelFactory):

    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    mobile = factory.Sequence(lambda n: '7765769{0}'.format(n))
    email_validated = True
    administrator_validated = True
    gender = 'F'
    profession = factory.SubFactory(ProfessionFactory)
    dob = date(1990, 12, 1)
