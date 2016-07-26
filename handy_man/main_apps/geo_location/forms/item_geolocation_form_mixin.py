from django import forms

from ..choices.district_polygons import districts_polygons
from ..choices.town_village_polygons import town_village_polygons
from ..choices.street_polygons import street_polygons


class ItemGeolocationMixinForm(object):
    def __init__(self, *args, **kwargs):
        super(ItemGeolocationMixinForm, self).__init__(*args, **kwargs)

    def clean(self):
        from ..models import TownVillage, Street
        from ..classes import Geolocation
        print("I got in here %%######################")

        district_name = self.cleaned_data.get('district', '')
        town_village_name = self.cleaned_data.get('town_village_name', '')
        street_name = self.cleaned_data.get('street_name', '')
        print(district_name, town_village_name, street_name)
        geolocation = Geolocation()
        district_polygon = None
        town_village_polygon = None
        street_polygon = None
        town_village = None
        street = None
        town_village_lat = 0
        town_village_lon = 0
        street_lat = 0
        street_lon = 0

        if not district_name:
            raise forms.ValidationError("The District name cannot be null.")

        if not town_village_name:
            raise forms.ValidationError("The Town/Village name cannot be null.")

        if not street_name:
            raise forms.ValidationError("The Street name cannot be null.")

        # Get the town
        try:
            town_village = TownVillage.objects.get(town_village_name=town_village_name)
            town_village_lat = town_village.center_latitude
            town_village_lon = town_village.center_longitude
        except TownVillage.DoesNotExist:
            pass

        # Get the street
        try:
            street = Street.objects.get(street_name=street_name)
            street_lat = street.center_latitude
            street_lon = street.center_longitude
        except Street.DoesNotExist:
            pass

        for key, value in districts_polygons.items():
            if key == district_name:
                district_polygon = value
                break

        for key, value in town_village_polygons.items():
            if key == town_village_name:
                town_village_polygon = value
                break

        for key, value in street_polygons.items():
            if key == street_name:
                street_polygon = value
                break

        town_in_district = geolocation.point_inside_polygon(town_village_lat, town_village_lon, district_polygon)
        street_in_town = geolocation.point_inside_polygon(street_lat, street_lon, town_village_polygon)
        item_latitude = self.cleaned_data.get('latitude', '')
        item_longitude = self.cleaned_data.get('longitude', '')
        item_in_street = geolocation.point_inside_polygon(item_latitude, item_longitude, street_polygon)

        if not town_in_district:
            raise forms.ValidationError("The town you selected is not in the district choosen.")
        if not street_in_town:
            raise forms.ValidationError("The street you selected is not in the town choosen.")
        if not item_in_street:
            raise forms.ValidationError("The location you selected is not in the street choosen.")
