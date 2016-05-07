from django.test import TestCase

from ..classes import Geolocation

from ..models import District, Street, TownVillage


class TestGeolocationMethods(TestCase):

    def setUp(self):
        self.geolocation = Geolocation()
        district_centers = {
            'north-west': [-19.330536, 23.588973], 'central': [-21.443605, 26.330152],
            'north-east': [-20.985286, 27.549635], 'gantsi': [-22.267728, 21.590500],
            'kgalagadi': [-24.725124, 21.820265], 'southren': [-24.804932, 24.709669],
            'kweneng': [-23.759405, 24.801545], 'south-east': [-24.947379, 25.759963],
            'kgatleng': [-24.198013, 26.354423]}
        self.create_districts(district_centers)
        south_east_district = District.objects.get(district_name='central')
        self.gaborone_town_village = TownVillage.objects.create(district=south_east_district, town_village_name='mmadinare', center_latitude=-21.869753, center_longitude=27.753179)
        self.street = Street.objects.create(town_village=self.gaborone_town_village, street_name='phase-2', center_latitude=-21.869753, center_longitude=27.753179)

    def create_districts(self, district_centers):
        """Create districts from a dictionary of district centers."""
        for key, value in district_centers.items():
            District.objects.create(district_name=key, center_latitude=value[0], center_longitude=value[1])

    def test_points_in_polygon(self):
        """Check if a point is in a polygon."""

        gps_lat = -24.644726
        gps_lon = 25.899749
        phase_two = [
            [-24.64589, 25.8851],
            [-24.647, 25.88673],
            [-24.64969, 25.88866],
            [-24.65146, 25.89131],
            [-24.65354, 25.89502],
            [-24.65593, 25.90044],
            [-24.64916, 25.90322],
            [-24.64077, 25.90672],
            [-24.63772, 25.90171],
            [-24.63241, 25.89701],
            [-24.64224, 25.88709]]
        self.assertTrue(self.geolocation.point_inside_polygon(gps_lat, gps_lon, phase_two))

    def test_points_outside_polygon(self):
        """Check if a point is outside a polygon."""

        gps_lat = -24.651352
        gps_lon = 25.908847
        phase_two = [
            [-24.64589, 25.8851],
            [-24.647, 25.88673],
            [-24.64969, 25.88866],
            [-24.65146, 25.89131],
            [-24.65354, 25.89502],
            [-24.65593, 25.90044],
            [-24.64916, 25.90322],
            [-24.64077, 25.90672],
            [-24.63772, 25.90171],
            [-24.63241, 25.89701],
            [-24.64224, 25.88709]]
        self.assertFalse(self.geolocation.point_inside_polygon(gps_lat, gps_lon, phase_two))

    def test_districts(self):
        """Test if districts list is return by the district class property."""
        self.assertEqual(District.objects.count(), 9)
        districts = ['south-east', 'southren', 'north-west', 'north-east', 'gantsi', 'central', 'kgalagadi', 'kgatleng', 'kweneng']
        for district in districts:
            self.assertTrue(district in self.geolocation.districts)

    def test_cernter_coordinates_district1(self):
        """Test if coordinates are returned giver a district name."""
        district_name = 'south-east'
        self.assertEqual(self.geolocation.cernter_coordinates(district_name), [-24.947379, 25.759963])

    def test_cernter_coordinates_district2(self):
        """Test if coordinates are returned are not of a town/village give a district."""
        district_name = 'south-east'
        self.assertNotEqual(self.geolocation.cernter_coordinates(district_name), [-24.605983, 25.933971])

    def test_center_coordinates_town_village(self):
        """Test if coordinates of a town are returned given a town_village name and a district name."""
        district_name = 'south-east'
        town_village_name = 'gaborone'
        self.assertEqual(self.geolocation.cernter_coordinates(district_name, town_village_name), [-24.605983, 25.933971])

    def test_center_coordinates_street(self):
        """Test if coordinates return are for a street, given, town/village, district, street."""
        district_name = 'south-east'
        town_village_name = 'gaborone'
        street_name = 'phase-2'
        self.assertEqual(self.geolocation.cernter_coordinates(district_name, town_village_name, street_name), [-24.644085, 25.896659])

    def test_distance_between_points(self):
        """Test if the correct distance between poits is calculated."""
        pass
