from geopy import Point
from geopy import distance


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
