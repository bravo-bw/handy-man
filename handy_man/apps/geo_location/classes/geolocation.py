from geopy import Point
from geopy import distance

from ..models import Street, TownVillage, District


class Geolocation:

    def point_inside_polygon(self, x, y, poly):
        """Determine if a point is inside a given polygon or not, Polygon is a list of (x,y) pairs."""

        n = len(poly)
        inside = False
        p1x, p1y = poly[0]
        for i in range(n + 1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def distance_between_points(self, lat, lon, lat_2, lon_2):
        """calculate the distance between two points in kilometers"""
        pt1 = Point(float(lat), float(lon))
        pt2 = Point(float(lat_2), float(lon_2))
        dist = distance.distance(pt1, pt2).km
        return dist

    def town_villages(self, district_name=None):
        """Return a list of towns."""
        town_villages = []
        district = None
        try:
            district = District.objects.get(district_name=district_name)
        except District.DoesNotExist:
            pass
        if district:
            town_village_qs = TownVillage.objects.filter(district=district)
        else:
            town_village_qs = TownVillage.objects.all()
        for tv in town_village_qs:
            town_villages.append(tv.town_village_name)
        return town_villages

    def streets(self, town_village_name=None):
        """Return a list of streets."""
        streets = []
        town_village = None
        try:
            town_village = TownVillage.objects.get(town_village_name=town_village_name)
        except TownVillage.DoesNotExist:
            pass
        if town_village:
            streets_qs = Street.objects.filter(town_village=town_village)
        else:
            streets_qs = Street.objects.all()
        for street in streets_qs:
            streets.append(street.street_name)
        return streets

    @property
    def districts(self):
        dist = []
        districts = District.objects.all()
        for district in districts:
            dist.append(district.district_name)
        return dist

    def cernter_coordinates(self, district_name=None, town_village_name=None, street_name=None):
        """Return the coordinates to center the map with."""
        coordinates = []
        if district_name and not town_village_name and not street_name:
            try:
                district = District.objects.get(district_name=district_name)
                coordinates = [district.center_latitude, district.center_longitude]
            except District.DoesNotExist:
                pass
        elif district_name and town_village_name and not street_name:
            try:
                town_village = TownVillage.objects.get(town_village_name=town_village_name)
                coordinates = [town_village.center_latitude, town_village.center_longitude]
            except TownVillage.DoesNotExist:
                pass
        elif district_name and town_village_name and street_name:
            try:
                street = Street.objects.get(street_name=street_name)
                coordinates = [street.center_latitude, street.center_longitude]
            except Street.DoesNotExist:
                pass
        return coordinates
