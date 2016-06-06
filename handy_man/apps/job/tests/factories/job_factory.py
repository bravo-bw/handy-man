import factory

from handy_man.apps.user_profile.tests.factories import UserProfileFactory
from handy_man.apps.job.tests.factories import JobTypeFactory

from ...models import Job, JobRequest


class JobFactory(factory.DjangoModelFactory):

    class Meta:
        model = Job

    posted_by = factory.SubFactory(UserProfileFactory)
    job_type = factory.SubFactory(JobTypeFactory)
    allocated_to = None
    status = 'new'
