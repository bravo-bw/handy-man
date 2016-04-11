from django.test import TestCase

from ..models import ItemGeolocationMixin


class TestModel(ItemGeolocationMixin):

    class Meta:
        app_label = 'handy_man'


class TestItemGeolocationMixin(TestCase):

    def setUp(self):
        self.item = TestModel.objects.create(latitude=24.124, longitude=22.343)

    def test_coordinates(self):
        """Check if coordinates are returned for an existing item."""

        self.assertEqual(self.coordinates, ['24.124', '22.343'])
