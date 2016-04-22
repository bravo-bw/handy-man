import factory

from ...models import Job


class JobFactory(factory.DjangoModelFactory):

    class Meta:
        model = Job

    posted_by = None
    allocated_to = None
    status = 'new'
    job_type = 'plumbing'
