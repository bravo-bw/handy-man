from django.test import TestCase

from ..models import ItemGeolocationMixin


class TestModel(ItemGeolocationMixin):

    class Meta:
        app_label = 'handy_man'


class TestItemGeolocationMixin(TestCase):

    def test_coordinates(self):
        pass
