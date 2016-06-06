import factory

from ...models import Quote, Job


class QuoteFactory(factory.DjangoModelFactory):

    class Meta:
        model = Quote

    job = factory.SubFactory(Job)
    currency = 'BWP'
    estimate_hours = 1.0
    rate_per_hour = 100.00
    amount = 100.00
    accepted = None

