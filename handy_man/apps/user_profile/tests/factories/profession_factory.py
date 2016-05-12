import factory

from ....main.choices import ARTISAN_PROFESSION
from ...models import Profession


class ProfessionFactory(factory.DjangoModelFactory):

    class Meta:
        model = Profession

    profession_type = ARTISAN_PROFESSION[0][0]

    qualified = True
