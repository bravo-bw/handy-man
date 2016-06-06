import factory

from ...models import Profession


class ProfessionFactory(factory.DjangoModelFactory):

    class Meta:
        model = Profession

    profession_type = factory.Sequence(lambda n: 'profession{0}'.format(n))
