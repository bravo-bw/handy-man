import factory

from ...models import Profession


class ProfessionFactory(factory.DjangoModelFactory):

    class Meta:
        model = Profession

    code = factory.Sequence(lambda n: 'CD{0}'.format(n))
    profession_type = factory.Sequence(lambda n: 'profession{0}'.format(n))
