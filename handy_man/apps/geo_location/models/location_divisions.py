from django.db import models


class District(models.Model):
    district_name = models.CharField(max_length=200)
    center_latitude = models.FloatField(
        verbose_name='Center Latitude',
        max_length=50,
        null=True,
        blank=True,)

    center_longitude = models.FloatField(
        verbose_name='Center Longitude',
        max_length=50,
        null=True,
        blank=True,)

    class Meta:
        app_label = 'geo_location'


class TownVillage(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    town_village_name = models.CharField(max_length=200)
    center_latitude = models.FloatField(
        verbose_name='Center Latitude',
        max_length=50,
        null=True,
        blank=True,)

    center_longitude = models.FloatField(
        verbose_name='Center Longitude',
        max_length=50,
        null=True,
        blank=True,)

    class Meta:
        app_label = 'geo_location'


class Street(models.Model):
    town_village = models.ForeignKey(TownVillage, on_delete=models.CASCADE)
    street_name = models.CharField(max_length=200)
    center_latitude = models.FloatField(
        verbose_name='Center Latitude',
        max_length=50,
        null=True,
        blank=True,)

    center_longitude = models.FloatField(
        verbose_name='Center Longitude',
        max_length=50,
        null=True,
        blank=True,)

    class Meta:
        app_label = 'geo_location'
