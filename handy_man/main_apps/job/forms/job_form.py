from django import forms

from handy_man.main_apps.job.models import Job

from handy_man.main_apps.geo_location.choices import districts_polygons, town_village_polygons, street_polygons


class JobForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)

    def clean(self):
        from handy_man.main_apps.geo_location.models import TownVillage, Street
        from handy_man.main_apps.geo_location.classes import Geolocation
        print("I got in here %%######################")
        cleaned_data = super(JobForm, self).clean()

        district_name = cleaned_data.get('district', '')
        town_village_name = cleaned_data.get('town_village', '')
        street_name = cleaned_data.get('street', '')
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
            if str(key) == str(district_name):
                print(key, "key value", district_name, 'matching form value')
                district_polygon = value
                print(district_polygon)
                break

        for key, value in town_village_polygons.items():
            if str(key) == str(town_village_name):
                town_village_polygon = value
                break

        for key, value in street_polygons.items():
            if str(key) == str(street_name):
                street_polygon = value
                break

        town_in_district = geolocation.point_inside_polygon(town_village_lat, town_village_lon, district_polygon)
        street_in_town = geolocation.point_inside_polygon(street_lat, street_lon, town_village_polygon)
        item_latitude = cleaned_data.get('latitude', '')
        item_longitude = cleaned_data.get('longitude', '')
        item_in_street = geolocation.point_inside_polygon(item_latitude, item_longitude, street_polygon)

        if not town_in_district:
            raise forms.ValidationError("The town you selected is not in the district choosen.")
        if not street_in_town:
            raise forms.ValidationError("The street you selected is not in the town choosen.")
        if not item_in_street:
            raise forms.ValidationError("The location you selected is not in the street choosen.")

    class Meta:
        model = Job
        fields = '__all__'
