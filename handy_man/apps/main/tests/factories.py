import factory
from django.contrib.auth.models import User

from ..choices import ACCOUNT_TYPE
from ..models import UserProfile, AccountDetails


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = User

    email = 'admin@gmail.com'
    first_name = factory.Sequence(lambda n: 'user{0}'.format(n))
    last_name = factory.Sequence(lambda n: 'user{0}'.format(n))
    username = factory.Sequence(lambda n: 'django{0}'.format(n))
#     password1 = '1'
#     password2 = '1'


class UserProfileFactory(factory.DjangoModelFactory):

    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    mobile = factory.Sequence(lambda n: '7765769{0}'.format(n))
    validated = True
    account = account=ACCOUNT_TYPE[0][1]


class AccountFactory(factory.DjangoModelFactory):

    class Meta:
        model = AccountDetails

    user_profile = factory.SubFactory(UserProfileFactory)
    account_number = factory.Sequence(lambda n: '7765769987{0}'.format(n))
    institution = factory.Sequence(lambda n: 'institution{0}'.format(n))
    payment_mode = factory.Sequence(lambda n: 'payment_mode{0}'.format(n))