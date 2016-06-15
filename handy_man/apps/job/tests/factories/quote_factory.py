import factory

from handy_man.apps.user_profile.tests.factories import UserProfileFactory

from ...models import Quote

from .job_factory import JobFactory


class QuoteFactory(factory.DjangoModelFactory):

    class Meta:
        model = Quote

    job = factory.SubFactory(JobFactory)
    artisan = factory.SubFactory(UserProfileFactory)
    currency = 'BWP'
    estimate_hours = 1.0
    amount = 100.00
    accepted = None
    closed_requoted = False

