import factory

from ...models import JobType


class JobTypeFactory(factory.DjangoModelFactory):

    class Meta:
        model = JobType

    code = factory.Sequence(lambda n: 'CD{0}'.format(n))
    name = factory.Sequence(lambda n: 'plumbing{0}'.format(n))
    rate_per_hour = 100.00
