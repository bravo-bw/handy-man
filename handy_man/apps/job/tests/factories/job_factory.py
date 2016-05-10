import factory

from handy_man.apps.user_profile.tests.factories import UserProfileFactory

from ...models import Job


class JobFactory(factory.DjangoModelFactory):

    class Meta:
        model = Job

    posted_by = factory.SubFactory(UserProfileFactory)
    allocated_to = None
    status = 'new'
    job_type = 'plumbing'
