import factory
from django.contrib.auth.models import User

from ...user_profile.tests.factories import UserProfileFactory
from ..choices import ACCOUNT_TYPE
from ..models import UserProfile, AccountDetails


class AccountFactory(factory.DjangoModelFactory):

    class Meta:
        model = AccountDetails

    user_profile = factory.SubFactory(UserProfileFactory)
    account_number = factory.Sequence(lambda n: '7765769987{0}'.format(n))
    institution = factory.Sequence(lambda n: 'institution{0}'.format(n))
    payment_mode = factory.Sequence(lambda n: 'payment_mode{0}'.format(n))